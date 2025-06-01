from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from datetime import date
from pydantic import BaseModel
from typing import List

from models import User,Attendance
from admin_router.auth.get_current_user import get_current_user

router = APIRouter()

@router.post("/attendance/first-check")
def first_attendance_check(user_id: int= Depends(get_current_user), db: Session = Depends(get_db)):
    # 여기선 단순히 출석 성공으로 가정
    from notify.post_alert import send_post_attendance_alert

    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        send_post_attendance_alert(user.name)
        return {"message": f"{user.name}님 출석 완료"}
    return {"error": "사용자를 찾을 수 없습니다."}

class CalendarRecord(BaseModel):
    date: date
    status: str

@router.get("/attendance/today")
def get_today_attendance(user_id: int= Depends(get_current_user), db: Session = Depends(get_db)):
    today = date.today()
    records = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.check_in >= today
    ).all()

    return [
        {
            "lecture_id": r.lecture_id,
            "status": r.status,
            "check_in": r.check_in.strftime("%H:%M")
        }
        for r in records
    ]

@router.get("/attendance/calendar", response_model=List[CalendarRecord])
def get_attendance_calendar(user_id: int= Depends(get_current_user), db: Session = Depends(get_db)):
    results = db.query(Attendance).filter(
        Attendance.user_id == user_id
    ).all()

    return [
        CalendarRecord(date=r.check_in.date(), status=r.status)
        for r in results
    ]


