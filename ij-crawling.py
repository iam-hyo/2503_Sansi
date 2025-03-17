from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import zipfile
import urllib.request
import time
import csv

# --- 1. ChromeDriver 다운로드 및 설정 ---
url = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/134.0.6998.88/win64/chromedriver-win64.zip'
zip_path = 'chromedriver.zip'
driver_dir = 'chromedriver_win64'

print("📥 ChromeDriver 다운로드 중...")
urllib.request.urlretrieve(url, zip_path)
print("✅ 다운로드 완료!")

# 압축 해제
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(driver_dir)
print("✅ 압축 풀기 완료!")

# ChromeDriver 경로 설정
driver_path = os.path.abspath(driver_dir + '/chromedriver.exe')
print("🔧 드라이버 경로:", driver_path)
print("파일 존재 여부:", os.path.exists(driver_path))

# --- 2. Selenium을 이용한 Google Maps 접속 ---
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')  # 브라우저 창 최대화
# options.add_argument('--headless')  # (필요 시) 헤드리스 모드 실행

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 리뷰를 수집할 장소의 Google Maps URL
url = "https://www.google.co.kr/maps/place/금돼지식당/data=!4m6!3m5!1s0x357ca3110d881915:0x66c78cca87fb7bda!8m2!3d37.5570994!4d127.0116712!16s%2Fg%2F11c0r5qrxn"
driver.get(url)
time.sleep(5)  # 페이지 로딩 대기

# --- 3. 리뷰 탭 클릭 ---
buttons = driver.find_elements(By.TAG_NAME, 'button')
for btn in buttons:
    if '리뷰' in btn.text or 'Reviews' in btn.text:
        btn.click()
        print("✅ 리뷰 탭 클릭 완료")
        time.sleep(5)  # 리뷰 로딩 대기
        break

# --- 4. 스크롤하여 리뷰 로드 ---
scroll_div = driver.find_element(By.CLASS_NAME, 'm6QErb')  # 스크롤 대상 요소 찾기
print("🔍 스크롤 대상 확인 완료")

for i in range(10):  # 10번 스크롤 (더 많은 리뷰를 원하면 숫자 조정)
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_div)
    print(f"🔽 스크롤 {i+1}회 완료")
    time.sleep(2)

# --- 5. 리뷰 데이터 추출 ---
review_blocks = driver.find_elements(By.CLASS_NAME, 'jftiEf')
print(f"\n📌 총 리뷰 블록 수: {len(review_blocks)}")

review_list = []
for idx, block in enumerate(review_blocks):
    try:
        author = block.find_element(By.CLASS_NAME, 'd4r55').text  # 작성자
        rating = block.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute('aria-label')  # 별점
        review = block.find_element(By.CLASS_NAME, 'wiI7pd').text  # 리뷰 내용
        print(f"{idx+1}. {author} | {rating} | {review[:30]}...")
        review_list.append([author, rating, review])
    except Exception as e:
        print(f"{idx+1}. 리뷰 추출 실패:", e)

# 브라우저 종료
driver.quit()

# --- 6. CSV 파일로 저장 ---
if review_list:
    with open("금돼지식당_리뷰.csv", "w", newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['작성자', '별점', '리뷰'])  # 헤더 작성
        writer.writerows(review_list)  # 데이터 저장
    print(f"\n✅ 총 {len(review_list)}개 리뷰 저장 완료 (금돼지식당_리뷰.csv)")
else:
    print("⚠️ 리뷰 없음 – CSV 저장 생략")
