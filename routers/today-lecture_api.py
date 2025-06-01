from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db

from models import Lecture, Enrollment
from admin_router.auth.get_current_user import get_current_user


router = APIRouter()
@router.get("/attendance/today-lecture")
def get_today_lecture(user_id: int= Depends(get_current_user), db: Session = Depends(get_db)):
    from datetime import datetime, time
    now = None
    now = datetime.now()
    today_weekday = now.strftime("%a")  # 'Mon', 'Tue', ..., 'Sun'
    
    weekday_map = {
        "Mon": "월", "Tue": "화", "Wed": "수", "Thu": "목",
        "Fri": "금", "Sat": "토", "Sun": "일"
    }
    korean_day = weekday_map[today_weekday]
    print(f"Today is: {korean_day}")
    now_time = now.time()
    print(now_time)
    # 오늘 해당 시간에 수강 중인 강의 찾기
    lecture = db.query(Lecture).join(Enrollment).filter(
        Enrollment.user_id == user_id,
        Lecture.day == korean_day,
        Lecture.start_time <= now_time,
        Lecture.end_time >= now_time
    ).first()

    if not lecture:
        return {
            "title": "오늘은 수업 없음",
            "day": "",
            "time": ""
            }


    return {
        "title": lecture.title,
        "day": korean_day,
        "time": f"{lecture.start_time.strftime('%H:%M')} - {lecture.end_time.strftime('%H:%M')}"
    }
