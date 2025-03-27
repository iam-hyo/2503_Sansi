from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import pandas as pd

# 1️⃣ 리뷰 추출 함수
def extract_reviews(driver, restaurant_name):
    try:
        # 1-1️⃣ 스크롤 영역 요소 찾기
        scroll_div = driver.find_element(By.CLASS_NAME, 'm6QErb')
        
        # 1-2️⃣ 10번 스크롤하여 리뷰 더 불러오기
        for i in range(10):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_div)
            print(f"🔽 스크롤 {i+1}회 완료")
            time.sleep(1)
    except:
        print("⚠️ 스크롤 요소를 찾을 수 없음")

    # 1-3️⃣ 리뷰 블록 찾기
    review_blocks = driver.find_elements(By.CLASS_NAME, 'jftiEf')
    review_list = []
    
    # 1-4️⃣ 각 리뷰 블록에서 작성자, 별점, 리뷰 내용 추출
    for block in review_blocks:
        try:
            author = block.find_element(By.CLASS_NAME, 'd4r55').text
            rating = block.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute('aria-label')
            review = block.find_element(By.CLASS_NAME, 'wiI7pd').text
            review_list.append([author, rating, review])
        except:
            continue

    return review_list

# 2️⃣ 리뷰 데이터를 Excel 파일로 저장하는 함수
def save_reviews_to_excel(review_data, search_query):
    save_path = os.path.join(os.path.dirname(os.getcwd()), f"{search_query}_리뷰.xlsx")

    # 2-1️⃣ ExcelWriter를 사용하여 여러 장소 리뷰 저장
    with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
        for name, reviews in review_data.items():
            df = pd.DataFrame(reviews, columns=['작성자', '별점', '리뷰'])
            df.to_excel(writer, sheet_name=name, index=False)

    print(f"✅ 총 {len(review_data)}개 장소 리뷰 저장 완료 ({save_path})")

# 3️⃣ 사용자에게 검색어 입력받기
search_query = input("검색할 장소를 입력하세요: ")

# 4️⃣ Selenium WebDriver 실행 및 브라우저 설정
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.co.kr/maps")
time.sleep(2)

# 5️⃣ 검색창 찾기 및 검색어 입력 후 실행
search_box = driver.find_element(By.ID, "searchboxinput")
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)
time.sleep(3)

# 6️⃣ 검색 결과 목록 가져오기
places = driver.find_elements(By.CLASS_NAME, 'Nv2PK')
place_names = [p.text.split("\n")[0] for p in places][:10]
print(f"📌 검색 결과: {len(place_names)}개 장소 발견")

# 7️⃣ 각 장소별 리뷰 수집
review_data = {}
for idx, place in enumerate(places[:10]):
    try:
        # 7-1️⃣ 장소 클릭하여 상세 페이지로 이동
        place.click()
        time.sleep(3)

        # 7-2️⃣ 리뷰 탭 클릭
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        for btn in buttons:
            if '리뷰' in btn.text or 'Reviews' in btn.text:
                btn.click()
                print(f"✅ {place_names[idx]} 리뷰 탭 클릭 완료")
                time.sleep(5)

                # 7-3️⃣ 리뷰 추출 함수 실행
                reviews = extract_reviews(driver, place_names[idx])
                review_data[place_names[idx]] = reviews
                break
    except:
        print(f"⚠️ {place_names[idx]} 리뷰 추출 실패")

# 8️⃣ WebDriver 종료
driver.quit()

# 9️⃣ 리뷰 데이터 Excel 파일로 저장 
save_reviews_to_excel(review_data, search_query)
