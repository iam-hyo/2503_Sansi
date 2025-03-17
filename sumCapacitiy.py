import pandas as pd

# CSV 파일 불러오기
file_path = "중구 대피소_최대수용인원.csv"
df = pd.read_csv(file_path, encoding="utf-8-sig")

# '최대 수용인원' 열에서 숫자만 추출하여 합산
df["최대 수용인원"] = df["최대 수용인원"].astype(str).str.replace("명", "", regex=True)
df["최대 수용인원"] = pd.to_numeric(df["최대 수용인원"], errors="coerce")  # 숫자가 아닌 값(NaN) 자동 처리

# 합산
total_capacity = df["최대 수용인원"].sum()

print(f"총 최대 수용 인원: {int(total_capacity):,}명")
