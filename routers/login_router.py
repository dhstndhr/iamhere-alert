# 예시: schemas.py 또는 routers/login_router.py 안에

from pydantic import BaseModel

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str

