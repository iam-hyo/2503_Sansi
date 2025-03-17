import requests
import csv

# API URL
url = "https://www.safekorea.go.kr/idsiSFK/neo/ext/json/evacuateList/evacuateList_3010000.json?datetime=20250316234034"
csv_file = "중구 대피소_최대수용인원.csv"
          
# 요청 헤더
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# API 요청
response = requests.get(url, headers=headers)

# 응답 데이터 확인
if response.status_code == 200:
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        csv_data = []
        
        for item in data:
            규모 = item.get("FACIL_POW")

            # 규모 값이 존재하고, 숫자인 경우만 계산
            if 규모 and isinstance(규모, (int, float)):  
                최대_수용인원 = round(규모 * 1.21)  # 계산 적용
            else:
                규모 = "정보 없음"
                최대_수용인원 = "정보 없음"

            csv_data.append({
                "위치": f"신주소: {item.get('FACIL_RD_ADDR', '정보 없음')}\n구주소: {item.get('FACIL_ADDR', '정보 없음')}",
                "시설": f"{item.get('FACIL_NM', '정보 없음')}\n({item.get('FACIL_GBN_NM', '정보 없음')})",
                "규모": f"{규모}㎡" if isinstance(규모, (int, float)) else 규모,
                "최대 수용인원": f"{최대_수용인원}명" if isinstance(최대_수용인원, (int, float)) else 최대_수용인원,
                "이동약자 접근성": "정보 없음"  # 공식 데이터에 없으므로 정보 없음 처리
            })


        # CSV 저장
        with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=["위치", "시설", "규모", "최대 수용인원", "이동약자 접근성"])
            writer.writeheader()
            writer.writerows(csv_data)

        print(f"CSV 파일이 저장되었습니다: {csv_file}")
    else:
        print("응답 데이터가 비어 있거나 리스트 형식이 아닙니다.")
else:
    print("데이터를 가져오지 못했습니다. 상태 코드:", response.status_code)
