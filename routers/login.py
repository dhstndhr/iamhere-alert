
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import LoginRequest, LoginResponse, User
from admin_router.auth.createToken import CreateToken
from datetime import datetime, timedelta
from db import get_db
router = APIRouter()

# DB에서 사용자 정보 가져오기
def get_user_from_db(db: Session, login_id: str):
    print(f"Attempting to fetch user with login_id: {login_id}")
    user = db.query(User).filter(User.login_id == login_id).first()
    if user:
        print(f"User found: {user.user_id})")
    else:
        print(f"User with login_id {login_id} not found.")
    return user

# 로그인 API 라우터
@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 사용자 확인
    user = db.query(User).filter(
        User.login_id == request.login_id,
        User.password == request.password
    ).first()
    #print(user.name,user.login_id, user.password)
    if not user:
        raise HTTPException(status_code=401, detail="잘못된 로그인 정보입니다.")


    # JWT 토큰 생성
    try:
        access_token = CreateToken(data={"sub": request.login_id, "user_id": user.user_id})
        print(f"Access token generated for user: {user.user_id}")
        # 응답 반환
        return LoginResponse(
        access_token= access_token,
        token_type= "bearer",
        user_name= user.name,
        user_id= str(user.user_id)
        )
    
    except Exception as e:
        print(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail="토큰 생성 중 오류가 발생했습니다.")    
    

