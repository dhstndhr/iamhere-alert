import jwt
from datetime import datetime, timedelta
from typing import Dict
import os
# config.py에서 설정 가져오기
SECRET_KEY = os.getenv("SECRET_KEY","mysecretkey")  # 기본값 설정
ALGORITHM = os.getenv("ALGORITHM")
#ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  

# JWT 토큰 생성 함수
def CreateToken(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    print("토큰생성함수")
    print(data)
    print(expires_delta)
    to_encode = data.copy()
    print(f"엔코드 데이터: {to_encode}")  # 디버깅용 출력
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    print(f"토큰 만료 시간: {expire}")  # 디버깅용 출력
    print("SECRET_KEY:", SECRET_KEY)  # 디버깅용 출력
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Token created with expiration: {expire}")
    print(f"Encoded JWT: {encoded_jwt}")  # 디버깅용 출력
    return encoded_jwt