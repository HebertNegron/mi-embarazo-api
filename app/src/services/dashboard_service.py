from models.dashboard_counts import DashboardCounts
from src.utils.mongo_conn import MongoConnection

class DashboardService:
    def get_dashboard_counts(self) -> DashboardCounts:
        with MongoConnection() as db:
            return DashboardCounts(
                doctors=db.users.count_documents({"role": "doctor"}),
                patients=db.patients.count_documents({}),
                appointments=db.appointments.count_documents({}),
            )