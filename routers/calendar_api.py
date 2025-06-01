from monitor.check_bluetooth_attendance import process_bluetooth_attendance
from fastapi import APIRouter, Depends
from models import Attendance
from sqlalchemy.orm import Session
from db import get_db
from admin_router.auth.get_current_user import get_current_user

router = APIRouter()
@router.get("/attendance/calendar")
def get_calendar_data(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(Attendance).filter(
        Attendance.user_id == user_id
    ).all()

    return [
        {
            "date": r.check_in.date().isoformat(),
            "status": r.status  # 예: '1차출석완료', '1차출석실패', '2차출석실패'
        }
        for r in records
    ]

