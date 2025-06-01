from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db import get_db
from models import User

# JWT 설정
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# OAuth2 스키마 (헤더에서 토큰 파싱)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("getcurrent_user called")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user = None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # 디코딩된 payload 확인
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        #print("현재 로그인한 사용자 ID:", user.user_id)

        # 문자열을 정수로 변환 (예: '1' → 1)
        user_id = int(user_id)
        
    except (JWTError, ValueError):
        raise credentials_exception

    #user = db.query(User).filter(User.user_id == user_id).first()
    #if user is None:
    #    raise credentials_exception

    return user_id  # 또는 user 전체를 반환하고 싶으면 return user
