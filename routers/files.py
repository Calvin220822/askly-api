from fastapi import APIRouter, HTTPException
from models import FileInfo
from db import get_conn
from datetime import datetime

router = APIRouter()

@router.post("/files")
def save_file(file_info: FileInfo):
    insert_sql = """
        INSERT INTO files (user_id, bucket, path, size, mime_type, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    try:
        with get_conn() as conn:
            cur = conn.cursor()
            now = datetime.utcnow()
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