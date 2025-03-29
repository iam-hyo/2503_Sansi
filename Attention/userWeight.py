import numpy as np

# 새로운 태그 목록 (tags2 기반)
tags = ['데이트', '혼밥', '가족식사', '노포', '주점', '양식', '일식', '중식', '분식', '한식', 
        '기타', '주차', '아동편의시설', '신식', '규모', '예약여부', '웨이팅', '매운정도', '가성비']

# 질문별 관련 태그 매핑 (선택지 개별 반영)
question_tag_map = {
    1: {"양식": 0, "중식": 0, "일식": 0, "분식": 0, "한식": 0},  
    2: {"데이트": 1, "혼밥": 1, "가족식사": 1, "주점": 1},
    3: {"노포": 1, "신식/노포": 1, "규모": 1, "가성비": 1},
    4: {"주차": 1, "예약여부": 1, "웨이팅": 1},
    5: {"매운정도": 1, "가성비": 1},
    6: {"아동편의시설": 1, "가족식사": 1},
}

# 사용자 응답 저장 딕셔너리
user_responses = {}

# 질문 목록 (선택지 포함)
questions = {
    1: "🍽️ 선호하는 음식 종류를 선택해주세요.\n   (0: 관심 없음 ~ 5: 매우 선호)\n   양식(🍕), 중식(🥡), 일식(🍣), 분식(🍜), 한식(🍚)",
    2: "👥 보통 누구와 식사하시나요?\n   ① 데이트 💑 ② 혼밥 🍽️ ③ 가족 식사 👨‍👩‍👧‍👦 ④ 술자리(주점) 🍻 (0~5 입력)",
    3: "🏚️ 신식과 노포 중 어느 쪽을 선호하시나요? (0: 신경 안 씀 ~ 5: 매우 중요)",
    4: "🚗 주차, 예약 가능 여부, 웨이팅을 얼마나 중요하게 생각하시나요? (0: 상관없음 ~ 5: 매우 중요)",
    5: "🌶️ 매운 음식을 얼마나 좋아하시나요? (0: 안 좋아함 ~ 5: 매우 좋아함)",
    6: "🧸 어린이 편의시설이 있는 곳을 선호하시나요? (0: 필요 없음 ~ 5: 매우 중요)"
}

# 사용자 입력 받기 (0~5점 사이, 예외처리 포함)
for q_num, question in questions.items():
    if q_num == 1 or q_num == 2:  # 여러 개 선택하는 질문
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

# 선택지 개별 반영 질문 (질문 1, 2번)
for q_num in [1, 2]:
    for tag, score in question_tag_map[q_num].items():
        tag_weights[tag] += score / max_score  # 0~1 정규화

# 정규화된 태그 가중치 출력
print("\n📌 사용자 선호도 기반 태그 가중치:")
for tag, weight in tag_weights.items():
    print(f"{tag}: {weight:.2f}")
