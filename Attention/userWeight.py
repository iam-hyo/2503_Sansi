import numpy as np

# 태그 목록
tags = [
    "맛", "느끼함", "노포", "가격", "거리",
    "친절", "주차", "양식", "중식", "일식",
    "데이트", "오마카세", "신선도", "대학생", "30대",
    "가족식사", "저녁", "웨이팅", "분식", "어린이 편의시설",
    "위생 및 청결", "시설", "실내 분위기", "40대", "맵기"
]

# 질문별 관련 태그 매핑 (선택지 개별 반영)
question_tag_map = {
    1: {"양식": 0, "중식": 0, "일식": 0, "분식": 0},  # 사용자의 선택별 점수 반영됨
    2: {"가격": 1, "대학생": 1, "30대": 1, "40대": 1},
    3: {"맛": 1, "느끼함": 1, "맵기": 1, "신선도": 1},
    4: {"실내 분위기": 1, "시설": 1, "위생 및 청결": 1},
    5: {"거리": 1, "주차": 1, "웨이팅": 1},
    6: {"데이트": 1, "가족식사": 1, "오마카세": 1, "어린이 편의시설": 1},
    7: {"노포": 1, "신선도": 1, "위생 및 청결": 1},
    8: {"친절": 1, "시설": 1, "위생 및 청결": 1},
    9: {"저녁": 1, "웨이팅": 1},
    10: {"맵기": 1, "맛": 1}
}

# 사용자 응답 저장 딕셔너리
user_responses = {}

# 질문 목록 (선택지 포함)
questions = {
    1: "🍽️ 다음 중 각 음식 종류에 대한 선호도를 입력해주세요.\n   (0: 관심 없음 ~ 5: 매우 선호)\n   양식(🍕), 중식(🥡), 일식(🍣), 분식(🍜)",
    2: "💰 식사 비용이 얼마나 중요한가요? (0: 상관없음 ~ 5: 매우 중요)",
    3: "😋 음식의 맛에서 가장 중요한 요소는 무엇인가요?\n   ① 느끼함 🧀 ② 매운맛 🌶️ ③ 신선도 🥗 ④ 감칠맛 🤤 (0~5 입력)",
    4: "🏠 식당의 분위기가 얼마나 중요한가요? (0: 신경 안 씀 ~ 5: 매우 중요)",
    5: "🚗 식당까지의 이동 거리가 얼마나 중요한가요? (0: 상관없음 ~ 5: 매우 중요)",
    6: "👨‍👩‍👧‍👦 어떤 상황에서 식당을 선택하는 경우가 많나요?\n   ① 데이트 💑 ② 가족 식사 👨‍👩‍👧‍👦 ③ 오마카세 🍣 ④ 어린이 편의시설 🧸 (0~5 입력)",
    7: "🏚️ 오래된 맛집(노포)과 신식 레스토랑 중 어느 쪽이 더 끌리나요? (0: 신경 안 씀 ~ 5: 매우 중요)",
    8: "😊 식당 직원의 친절함이 얼마나 중요한가요? (0: 신경 안 씀 ~ 5: 매우 중요)",
    9: "🌙 주로 언제 식사를 하시나요? (0: 시간 상관없음 ~ 5: 특정 시간대 매우 중요)",
    10: "🔥 매운 음식을 얼마나 좋아하시나요? (0: 안 좋아함 ~ 5: 매우 좋아함)"
}

# 사용자 입력 받기 (0~5점 사이, 예외처리 포함)
for q_num, question in questions.items():
    if q_num == 1 or q_num == 6:  # 여러 개 선택하는 질문
        print(question)
        for tag in question_tag_map[q_num]:
            while True:
                try:
                    user_input = input(f"   {tag}: ").strip()
                    score = int(user_input) if user_input else 0
                    if score < 0 or score > 5:
                        raise ValueError
                    question_tag_map[q_num][tag] = score  # 개별 가중치 적용
                    break
                except ValueError:
                    print("⚠️ 0에서 5 사이의 숫자를 입력해주세요!")
    else:
        while True:
            try:
                user_input = input(f"{question} (0~5, Enter 입력 시 기본값 0): ").strip()
                score = int(user_input) if user_input else 0
                if score < 0 or score > 5:
                    raise ValueError
                user_responses[q_num] = score
                break
            except ValueError:
                print("⚠️ 0에서 5 사이의 숫자를 입력해주세요!")

# 태그별 가중치 계산
tag_weights = {tag: 0 for tag in tags}

# 일반 질문 반영 (0~1로 정규화)
max_score = 5
for question, score in user_responses.items():
    normalized_score = score / max_score
    for tag in question_tag_map[question]:
        tag_weights[tag] += normalized_score

# 선택지 개별 반영 질문 (질문 1, 6번)
for q_num in [1, 6]:
    for tag, score in question_tag_map[q_num].items():
        tag_weights[tag] += score / max_score  # 0~1 정규화

# 정규화된 태그 가중치 출력
print("\n📌 사용자 선호도 기반 태그 가중치:")
for tag, weight in tag_weights.items():
    print(f"{tag}: {weight:.2f}")
