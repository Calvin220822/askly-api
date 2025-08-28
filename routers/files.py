from fastapi import APIRouter, HTTPException
from models import FileInfo, PresignedURLRequest
from db import get_conn
from datetime import datetime
from supabase import create_client
import os
from urllib.parse import unquote
from storage3.exceptions import StorageApiError

router = APIRouter()

supabase = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_SERVICE_KEY", "")
)

# get presigned URL for file upload
@router.post("/file/presigned_url")
def get_presigned_url(request: PresignedURLRequest):
    try:
        # Verify bucket exists
        buckets = supabase.storage.list_buckets()
        print(buckets)
        if not any(bucket.name == request.bucket for bucket in buckets):
            raise HTTPException(
                status_code=404,
                detail=f"Bucket '{request.bucket}' not found"
            )

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        decoded_filename = unquote(request.file_name)
        safe_filename = "".join(c for c in decoded_filename if c.isalnum() or c in ('-', '_', '.'))
        
        file_path = f"user_uploads/{timestamp}_{safe_filename}"

        # Create signed URL
        signed_url = supabase.storage.from_(request.bucket).create_signed_url(
            path=file_path,
            expires_in=3600,
            options={
                "content-type": "application/octet-stream",
                "upsert": "true"
            }
        )

        if not signed_url:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate signed URL"
            )

        return {"upload_url": signed_url, "file_path": file_path}

    except StorageApiError as e:
        raise HTTPException(
            status_code=e.statusCode,
            detail=f"Storage API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/file/save_metadata")
def save_file(file_info: FileInfo):
    insert_sql = """
        INSERT INTO files (user_id, bucket, path, size, mime_type, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    try:
        with get_conn() as conn:
            cur = conn.cursor()
            now = datetime.now()
            cur.execute(
                insert_sql,
                (
                    file_info.user_id,
                    file_info.bucket,
                    file_info.path,
                    file_info.size,
                    file_info.mime_type,
                    now,
                    now,
                ),
            )
            row = cur.fetchone()
            conn.commit()
            cur.close()
            file_id = row[0] if row else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "code": 0,
        "message": "File info saved successfully",
        "data": {
            "id": file_id,
            "user_id": file_info.user_id,
            "bucket": file_info.bucket,
            "path": file_info.path,
            "size": file_info.size,
            "mime_type": file_info.mime_type,
            "created_at": now.timestamp(),
            "updated_at": now.timestamp(),
        },
    }