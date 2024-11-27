from pydantic import BaseModel


class DashboardCounts(BaseModel):
    doctors: int
    patients: int
    appointments: int
