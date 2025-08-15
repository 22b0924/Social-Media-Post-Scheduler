from pydantic import BaseModel
from typing import List
from datetime import datetime

class ScheduleRequest(BaseModel):
    platform: str        # e.g., "twitter" or "linkedin" (comma allowed)
    content: str
    post_at: str         # ISO timestamp or "YYYY-MM-DD HH:MM"

class PostOut(BaseModel):
    id: int
    platform: str
    content: str
    post_at: str
    created_at: str
    status: str
    result: str = None
