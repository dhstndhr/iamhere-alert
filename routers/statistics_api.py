from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Attendance
from datetime import date, timedelta
from admin_router.auth.get_current_user import get_current_user
router = APIRouter()

@router.get("/attendance/statistics")
def get_statistics(user_id: int=Depends(get_current_user), db: Session = Depends(get_db)):
    # 전체 통계
    attended = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.status == "1차출석완료"
    ).count()

    late = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.status == "1차출석실패"
    ).count()

    missed = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.status == "2차출석실패"
    ).count()

    total = attended + late + missed
    attendance_rate = round((attended / total) * 100, 1) if total > 0 else 0.0

    # 이번 주 출석 수 계산
    today = date.today()
    monday = today - timedelta(days=today.weekday())  # 이번 주 월요일

    weekly_attended = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.status == "1차출석완료",
        Attendance.check_in >= monday
    ).count()

    return {
        "attended": attended,
        "late": late,
        "missed": missed,
        "total_lectures": total,
        "attendance_rate": attendance_rate,
        "weekly_attended": weekly_attended
    }

