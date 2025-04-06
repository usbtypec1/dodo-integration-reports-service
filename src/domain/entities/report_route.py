from uuid import UUID

from pydantic import BaseModel


class ReportRoute(BaseModel):
    chat_id: int
    report_type_id: str
    report_type_name: str
    unit_id: UUID


class ReportRouteListResponse(BaseModel):
    routes: list[ReportRoute]
    is_end_of_list_reached: bool
