import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from monitor.monitor_second_check import monitor_attendance
from scheduler.scheduler import start_scheduler

from routers import bluetooth_api, second_check_api, attendance_api, statistics_api, login

from fastapi.middleware.cors import CORSMiddleware

from admin_router import attendance, summary, alerts
from fastapi.openapi.utils import get_openapi
#from scheduler import monitor_attendance
#from scheduler import start_schedule

swagger_ui_init_oauth = {"usePkceWithAuthorizationCodeGrant": False}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        start_scheduler()
        asyncio.create_task(monitor_attendance())
        print("✅ 스케줄러 및 감시 작업 시작됨")
        yield
    except Exception as e:
        print(f"❌ lifespan 내부 오류: {e}")
        yield
    
    
app = FastAPI(lifespan=lifespan,swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": False})

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="myapi",
        version="1.0.0",
        description="API with JWT Authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema   
app.openapi = custom_openapi




# ✅ CORS 허용 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Android 앱에서 접속 가능하도록 전체 허용 (*). 운영 시엔 IP로 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index():
    return "출석 알람 시스템 작동 중입니다!"





app.include_router(second_check_api.router)
app.include_router(bluetooth_api.router)
app.include_router(attendance_api.router)
app.include_router(statistics_api.router)
app.include_router(attendance.router)
app.include_router(summary.router)
app.include_router(alerts.router)
app.include_router(login.router)
