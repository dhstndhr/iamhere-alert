from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import json

# 서비스 계정 키 파일 경로
SERVICE_ACCOUNT_FILE = "credentials/firebase-key.json"

# 메시지 전송 대상 토큰
#TARGET_TOKEN = "ds9pxuaKQj-evFC5Zkg-Bw:APA91bE1Nf0oPwpA6Hfw3GKqdcjIumCs02Rqx7tkuOezxnZ_geZCdvM5bWZVWXzHRb2d0p_0V6-mflMmMeFUDeH5Nu7fDfrHBYJDzcuusWlLJuE5910KZiQ"

TARGET_TOKEN = "f_Jq0BwTRu2hkQUkqkD1MX:APA91bG35kH9jbk1FXlvL2_Yw32c1jD84aJmWRObFT-S08fIy6yPkk5rWvS6hGV8-elhMrXBCz4k5zzqzZgiaFTvCsS8Aro-WcnIic8e1dELTUC-uYjiNYw"

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    return credentials.token

def send_fcm_v1(token: str, title: str, body: str):
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }

    message = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    project_id = "i-am-here-458403"
    url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    response = requests.post(url, headers=headers, data=json.dumps(message))
    print(f"✅ FCM 응답: {response.status_code} / {response.text}")

# 테스트 실행
send_fcm_v1(TARGET_TOKEN, "2차 출석 요청", "지문 인증을 해주세요!")


