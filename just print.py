import requests
from datetime import datetime, timedelta

API_KEY = "004c7c516b0263e5aa95f9db6df5bd47bb556e57e61248e3f127a8fb0e9fffbd"

STN_ID = "108"

SUBMISSION_DATE_STR = "20251120"  # <--- 여기를 실제 제출일로 수정하세요!


# ===============================================================

def call_weather_api(start_dt, start_hh, end_dt, end_hh):
    """
    기상청 종관기상관측(ASOS) 시간자료 API를 호출하여 데이터를 출력합니다.
    """
    # API 엔드포인트 (기상청 종관기상관측 시간자료 조회)
    url = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"

    # 요청 파라미터 설정
    params = {
        "serviceKey": API_KEY,  # 인증키
        "pageNo": "1",  # 페이지 번호
        "numOfRows": "100",  # 한 페이지 결과 수
        "dataType": "JSON",  # 응답 자료 형식 (JSON)
        "dataCd": "ASOS",  # 자료 분류 코드
        "dateCd": "HR",  # 날짜 분류 코드 (시간)
        "startDt": start_dt,  # 조회 기간 시작일 (YYYYMMDD)
        "startHh": start_hh,  # 조회 기간 시작시 (HH)
        "endDt": end_dt,  # 조회 기간 종료일 (YYYYMMDD)
        "endHh": end_hh,  # 조회 기간 종료시 (HH)
        "stnIds": STN_ID  # 지점 번호
    }

    print(f"\n>>> 데이터 요청: {start_dt} {start_hh}시 ~ {end_dt} {end_hh}시 (지점: {STN_ID})")

    try:
        # API 호출 (requests 라이브러리가 파라미터를 인코딩하여 전송함)
        response = requests.get(url, params=params)

        # 응답 상태 코드 확인
        if response.status_code == 200:
            # JSON 데이터 파싱 시도
            try:
                data = response.json()
                # 결과가 정상적인지 체크 (response header 코드 확인)
                header_code = data.get('response', {}).get('header', {}).get('resultCode')

                if header_code == '00':
                    items = data['response']['body']['items']['item']
                    print("✅ 조회 성공!")
                    for item in items:
                        # 필요한 정보만 간략히 출력 (일시, 기온, 강수량 등)
                        print(f"  - 일시: {item.get('tm')} | 기온: {item.get('ta')}°C | 습도: {item.get('hm')}%")
                else:
                    print(f"⚠️ API 에러 메시지: {data.get('response', {}).get('header', {}).get('resultMsg')}")
                    print("  (인증키가 아직 등록되지 않았거나, 트래픽이 초과되었을 수 있습니다.)")

            except Exception as parse_error:
                # JSON 변환 실패 시 텍스트로 출력 (XML일 경우 등)
                print(f"⚠️ 응답을 JSON으로 변환할 수 없습니다. 원본 응답:\n{response.text[:200]}...")
        else:
            print(f"❌ HTTP 요청 실패: {response.status_code}")

    except Exception as e:
        print(f"❌ 프로그램 실행 중 오류 발생: {e}")



if __name__ == "__main__":
    print(f"--- API 데이터 추출 시작 (종관번호: {STN_ID}) ---")

    # 1. 2024년 12월 04일 15시 ~ 18시
    call_weather_api(start_dt="20241204", start_hh="15", end_dt="20241204", end_hh="18")

    # 2. 2025년 06월 04일 12시 ~ 16시
    call_weather_api(start_dt="20250604", start_hh="12", end_dt="20250604", end_hh="16")

    try:
        submit_date = datetime.strptime(SUBMISSION_DATE_STR, "%Y%m%d")
        target_date = submit_date - timedelta(days=2)
        target_date_str = target_date.strftime("%Y%m%d")

        print(f"\n[자동 계산] 제출일({SUBMISSION_DATE_STR})의 이틀 전은 {target_date_str} 입니다.")
        call_weather_api(start_dt=target_date_str, start_hh="00", end_dt=target_date_str, end_hh="03")

    except ValueError:
        print("\n❌ 날짜 형식이 잘못되었습니다. SUBMISSION_DATE_STR 변수를 'YYYYMMDD' 형식으로 확인해주세요.")
