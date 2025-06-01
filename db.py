# db.py
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,Session
from config import DB_CONFIG

DATABASE_URL = "mysql+pymysql://teamuser:0718@34.64.121.178:3306/iamhere"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ FastAPI 의존성 주입용 get_db
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

# import pymysql
# from config import DB_CONFIG  # config.py에서 DB 설정 불러오기

# 데이터베이스 연결 함수
def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        charset=DB_CONFIG["charset"],
        cursorclass=pymysql.cursors.DictCursor
    )

try:
    conn = get_db_connection()
    print("✅ 외부 DB 연결 성공!")
    conn.close()
except Exception as e:
    print("❌ 연결 실패:", e)

# # 테이블 생성 함수
# def initialize_database():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # users 테이블
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
#             student_id VARCHAR(100) NOT NULL,
#             name VARCHAR(100) NOT NULL,
#             major VARCHAR(255) NOT NULL
#         )
#     """)

#     # lectures 테이블
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS lectures (
#             lecture_id BIGINT PRIMARY KEY AUTO_INCREMENT,
#             title VARCHAR(255) NOT NULL,
#             day ENUM('월','화','수','목','금') NOT NULL,
#             start_time TIME NOT NULL,
#             end_time TIME NOT NULL,
#             start_date DATE NOT NULL,
#             end_date DATE NOT NULL
#         )
#     """)

#     # fingerprints 테이블
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS fingerprints (
#             user_id BIGINT PRIMARY KEY NOT NULL,
#             fingerprint_template TEXT NOT NULL,
#             FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
#         )
#     """)

#     # bluetooth_devices 테이블
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS bluetooth_devices (
#             device_id BIGINT PRIMARY KEY AUTO_INCREMENT,
#             user_id BIGINT NOT NULL,
#             mac_address VARCHAR(17) UNIQUE NOT NULL,
#             device_name VARCHAR(255),
#             registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
#         )
#     """)

#     # enrollments 테이블
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS enrollments (
#             enrollment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
#             user_id BIGINT NOT NULL,
#             lecture_id BIGINT NOT NULL,
#             FOREIGN KEY (user_id) REFERENCES users(user_id),
#             FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id) ON DELETE CASCADE,
#             UNIQUE(user_id, lecture_id)
#         )
#     """)

#     # attendances 테이블
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS attendances (
#             attendance_id BIGINT PRIMARY KEY AUTO_INCREMENT,
#             user_id BIGINT,
#             lecture_id BIGINT,
#             method ENUM('Bluetooth', 'Fingerprint', 'Both') NOT NULL,
#             mac_address VARCHAR(17),
#             check_in TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             status ENUM('1차출석완료', '1차출석실패', '2차출석완료', '2차출석실패', '2차출석제외') NOT NULL,
#             FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
#             FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id) ON DELETE SET NULL,
#             FOREIGN KEY (mac_address) REFERENCES bluetooth_devices(mac_address) ON DELETE SET NULL
#         )
#     """)

#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     print("🔧 데이터베이스를 초기화합니다...")
#     initialize_database()
#     print("✅ 데이터베이스가 준비되었습니다.")
