from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Attendance, User
from db import get_db
from .schemas import AttendanceResponse, UpdateAttendance
from typing import List
from notify.fcm import send_fcm_v1

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/attendances", response_model=List[AttendanceResponse])
def get_all_attendances(db: Session = Depends(get_db)):
    records = (
        db.query(Attendance, User)
        .join(User, Attendance.user_id == User.user_id)
        .all()
    )

    return [
        AttendanceResponse(
            attendance_id=a.attendance_id,
            name=u.name,
            student_id=str(u.user_id), #student_id=>u.userID,
            status=a.status,
            check_in=a.check_in
        )
        for a, u in records
    ]


@router.put("/attendance/{attendance_id}")
def update_attendance(attendance_id: int, data: UpdateAttendance, db: Session = Depends(get_db)):
    record = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance not found")

    record.status = data.status
    db.commit()
    return {"message": "updated"}

from notify.fcm import send_fcm_v1

@router.get("/test-alert")
def test_alert():
    send_fcm_v1(
        token="ds9pxuaKQj-evFC5Zkg-Bw:APA91bE1Nf0oPwpA6Hfw3GKqdcjIumCs02Rqx7tkuOezxnZ_geZCdvM5bWZVWXzHRb2d0p_0V6-mflMmMeFUDeH5Nu7fDfrHBYJDzcuusWlLJuE5910KZiQ",
        title="🔔 출석 확인 요청",
        body="홍길동 학생, 지금 지문 인증을 진행해주세요."
    )
    return {"message": "알림 전송 완료"}
