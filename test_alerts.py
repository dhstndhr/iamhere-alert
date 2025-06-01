from notify.post_alert import (
    send_second_post_alert,
    send_second_fail_alert,
    send_result_alert,
    send_post_attendance_alert, send_post_fail_alert
)

from notify.pre_alert import send_second_alert

if __name__ == "__main__":
    # 개별 테스트 시 이곳만 수정하면 됨
    #print("🔍 2차 출석 성공 알림 테스트")
    #send_second_post_alert("홍길동")

    #print("\n🔍 2차 출석 실패 알림 테스트")
    #send_second_fail_alert("김철수")

    #print("\n🔍 지문 인증 결과 알림 테스트")
    #send_result_alert("이영희", True)
    #send_result_alert("박민수", False)


    #print("🔍 출석 성공 알림 테스트")
    #send_post_attendance_alert("이영희")

    #print("🔍 출석 실패 알림 테스트")
    #send_post_fail_alert("박민수")

    # ✅ 2차 출석 요청 알림 테스트
    print("\n🔍  2차 출석 요청 알림 테스트")
    send_second_alert("김철수", "자료구조")

