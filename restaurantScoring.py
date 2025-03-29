import pandas as pd
import os
from recomandRestaurant.userWeight import get_user_weights

def recommend_restaurants(csv_path, user_weights, top_n=5):
    # CSV 파일 로드 (매개변수로 받은 경로 사용)
    df = pd.read_csv(csv_path)
    
    # 식당별 점수 계산
    df["총점"] = df.drop(columns=["가게명"]).apply(lambda row: sum(row[tag] * user_weights.get(tag, 0) for tag in user_weights), axis=1)
    
    # 상위 N개 식당 추천
    top_restaurants = df.sort_values(by="총점", ascending=False).head(top_n)
    return top_restaurants[["가게명", "총점"]]

if __name__ == "__main__":
    user_weights = get_user_weights()  # 사용자 가중치 불러오기
    
    # CSV 파일 경로 지정 (예시로 절대 경로 사용)
    csv_path = './tfidf_result.csv'  # 또는 절대 경로로 지정
    
    recommended = recommend_restaurants(csv_path, user_weights)
    print(recommended)
