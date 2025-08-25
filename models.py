from pydantic import BaseModel
from typing import Optional

class AgentCreate(BaseModel):
    name: str
    visibility: Optional[str] = "private"

class AgentSave(BaseModel):
    id: Optional[str]
    name: Optional[str]
    visibility: Optional[str] = "private"
    temperature: Optional[float] = 0
    max_tokens: Optional[int] = 1000
    instructions: Optional[str]
    model: Optional[str] = "gpt-3.5-turbo"

class FileInfo(BaseModel):
    user_id: str
    bucket: str
    path: str
    size: int
    mime_type: str