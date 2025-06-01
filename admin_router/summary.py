# admin_router/summary.py
from fastapi import APIRouter, Depends, HTTPException
from models import Lecture, User, Professor
from sqlalchemy.orm import Session
from db import get_db
from models import Attendance
from sqlalchemy import desc
from sqlalchemy import func
from datetime import datetime, timedelta
from admin_router.auth.get_current_user import get_current_user
router = APIRouter(prefix="/admin", tags=["admin"])

# 요일 순서: 월 -> 화 -> 수 -> 목 -> 금
week_days = ['월', '화', '수', '목', '금']

# 요일 매핑 (오늘 요일을 기준으로 0: 월요일, 1: 화요일, ...)
day_mapping = {
    'Mon': 0,  # 월요일
    'Tue': 1,  # 화요일
    'Wed': 2,  # 수요일
    'Thu': 3,  # 목요일
    'Fri': 4,  # 금요일
    'Sat': 0,  # 토요일 (월요일부터 시작하도록 처리)
    'Sun': 0,  # 일요일 (월요일부터 시작하도록 처리)
}
# 현재 요일을 구하는 함수
def get_current_day():
    return datetime.today().strftime('%a')  # 오늘 요일 (Mon, Tue 등)

# 교수의 가장 최근 강의를 찾는 함수
def get_recent_lecture(db: Session, professor_user_id: int):
    current_day = get_current_day()  # 오늘 요일
    start_day_index = day_mapping[current_day]  # 오늘 요일의 인덱스
    print(f"오늘 요일: {current_day}, 인덱스: {start_day_index}")
    # 요일 순서대로 강의를 찾아봄 (월 -> 화 -> 수 -> ...)
    for i in range(5):  # 5일을 돌아가면서 찾음
        day_to_check = week_days[(start_day_index + i) % 5]  # 순차적으로 요일을 찾아가며
        print(f"[LOG] 체크할 요일: {day_to_check} (index {day_to_check})")
        lecture = (
            db.query(Lecture)
            .filter(Lecture.professor_id == professor_user_id)
            .filter(Lecture.day == day_to_check)  # 해당 요일에 해당하는 강의 찾기
            .first()
        )
          #  .filter(Lecture.start_time <= datetime.now().time())  # 현재 시간보다 시작 시간이 이전인 강의
           # .order_by(desc(Lecture.start_time))  # 시간 기준 내림차순 정렬
            
        
        if lecture:
            return lecture  # 강의를 찾으면 바로 반환

def get_recent_lecture_date(lecture_day: str, start_date: datetime.date, end_date: datetime.date) -> datetime.date:
    """
    오늘을 기준으로 과거에 열렸던 가장 최근의 요일(lecture_day)을 구함.
    예: 오늘이 금요일이고, lecture_day가 '목'이면 -> 어제 날짜가 반환됨.
    """

    # 요일 매핑 (0=월, 6=일)
    day_map = {'월': 0, '화': 1, '수': 2, '목': 3, '금': 4}

    if lecture_day not in day_map:
        raise ValueError("올바르지 않은 요일입니다.")

    target_weekday = day_map[lecture_day]
    today = datetime.today().date()

    for i in range(7):  # 최근 일주일 내에서 해당 요일을 찾음
        candidate = today - timedelta(days=i)
        if candidate.weekday() == target_weekday and start_date <= candidate <= end_date:
            return candidate

    return None  # 해당 요일이 없는 경우

@router.get("/summary")
def get_lecture_summary(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. 교수인지 확인
    professor = db.query(User).filter(User.user_id == user_id).first()
    if not professor or professor.role != "교수":
        raise HTTPException(status_code=403, detail="교수가 아닙니다.")

    # 2. 해당 교수의 가장 최근 강의 조회
    lecture = get_recent_lecture(db, professor.user_id)
    if not lecture:
        raise HTTPException(status_code=404, detail="해당 교수의 강의가 없습니다.")

    # 3. 출석 통계 집계
    attended = db.query(Attendance).filter(
        Attendance.lecture_id == lecture.lecture_id,
        Attendance.status.in_(["1차출석완료", "2차출석완료"])
    ).count()

    late = db.query(Attendance).filter(
        Attendance.lecture_id == lecture.lecture_id,
        Attendance.status == "1차출석실패"
    ).count()

    absent = db.query(Attendance).filter(
        Attendance.lecture_id == lecture.lecture_id,
        Attendance.status.in_(["2차출석실패", "2차출석제외"])
    ).count()

    total = db.query(Attendance.user_id).filter(
        Attendance.lecture_id == lecture.lecture_id,
    ).distinct().count()

    lecture_date = get_recent_lecture_date(lecture.day, lecture.start_date, lecture.end_date)
    lecture_date_str = lecture_date.strftime("%Y.%m.%d") if lecture_date else "강의 없음"

    return {
        "total": total,
        "attended": attended,
        "late": late,
        "absent": absent,
        "lecture_date": lecture_date_str,
        "lecture_info": f"({lecture.title} {lecture.start_time}-{lecture.end_time})"
    }
"""
def get_summary(db: Session = Depends(get_db)):
    total = db.query(Attendance.user_id).distinct().count()
    attended = db.query(Attendance).filter(Attendance.status.in_(["1차출석완료", "2차출석완료"])).count()
    late = db.query(Attendance).filter(Attendance.status == "1차출석실패").count()
    absent = db.query(Attendance).filter(Attendance.status.in_(["2차출석실패", "2차출석제외"])).count()

    return {
        "total": total,
        "attended": attended,
        "late": late,
        "absent": absent,
        "lecture_date": "2025.05.03",  # 필요 시 lecture 테이블과 조인
        "lecture_info": "캡스톤 디자인 (수) 09:00-12:00"
    }

"""