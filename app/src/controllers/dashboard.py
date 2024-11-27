from fastapi import APIRouter, Depends
from models.dashboard_counts import DashboardCounts
from services.dashboard_service import DashboardService
from utils.login_required import login_required

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[
        Depends(
            login_required
        )
    ]
)


@dashboard_router.get("/counts")
def get_counts() -> DashboardCounts:
    return DashboardService().get_dashboard_counts()