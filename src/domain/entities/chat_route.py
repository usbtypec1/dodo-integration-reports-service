from uuid import UUID

from pydantic import BaseModel


class ChatRoute(BaseModel):
    chat_id: int
    unit_ids: tuple[UUID, ...]
    report_type_id: str
