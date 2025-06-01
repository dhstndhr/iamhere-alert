# DB_CONFIG = {
#     "host": "localhost",
#     "user": "test",
#     "password": "test1234",
#     "database": "test_db",
#     "charset": "utf8mb4"
# }

# FINGERPRINT_SENSOR_PORT = "/dev/ttyAMA0"
# FINGERPRINT_BAUDRATE = 57600

DB_CONFIG = {
    "host": "34.64.121.178",        # 외부 DB IP
    "user": "teamuser",
    "password": "0718",
    "database": "iamhere",
    "charset": "utf8mb4"
}
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256" # 24시
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24시간