import numpy as np

tags = ['데이트', '혼밥', '가족식사', '노포', '주점', '양식', '일식', '중식', '분식', '한식',
        '주차', '아동편의시설', '신식', '규모', '예약여부', '웨이팅', '매운정도', '가성비']

question_tag_map = {
    1: {"양식": 0, "중식": 0, "일식": 0, "분식": 0, "한식": 0},  
    2: {"데이트": 0, "혼밥": 0, "가족식사": 0, "주점": 0},
    3: {"노포": 0, "신식": 0},
    4: {"주차": 1, "예약여부": 1, "웨이팅": 1},
    5: {"매운정도": 1},
    6: {"아동편의시설": 1, "가족식사": 1},
    7: {"가성비": 1},
}

def get_user_weights():
    """사용자의 답변을 바탕으로 태그 가중치를 계산하여 반환"""
    tag_weights = {tag: 0 for tag in tags}
    
    # 사용자 응답 저장용 변수
    user_responses = {}

    # 1번 문항: 음식 종류 선호도 (0~5 점수 입력)
    for tag in question_tag_map[1]:
        tag_weights[tag] += question_tag_map[1][tag] / 5  

    # 2, 3번 문항: 특정 목적 및 분위기 선호도 반영
    for tag in question_tag_map[2]:
        tag_weights[tag] += question_tag_map[2][tag] / 5  

    for tag in question_tag_map[3]:
        tag_weights[tag] += question_tag_map[3][tag] / 5  

    # 6번 문항: 아동편의시설 & 가족식사 중요도 반영
    child_facility_score = user_responses.get(6, 0)
    family_meal_score = question_tag_map[2].get("가족식사", 0)
    tag_weights["규모"] += (child_facility_score + family_meal_score) / 10

    return tag_weights

user_responses = {}

questions = {
    1: "각 음식 종류별로 선호도를 입력해주세요.\n   (0: 관심 없음 ~ 5: 매우 선호)\n   예: 양식, 중식, 일식, 분식, 한식",
    2: "가장 부합하는 식사 목적을 1순위와 2순위로 선택해주세요.\n   ① 데이트 ② 혼밥 ③ 가족 식사 ④ 술자리(주점)",
    3: "전통 있는 ‘노포(老舗)’와 현대적인 ‘신식’ 레스토랑 중 어디가 더 끌리시나요?\n   (0: 신식 선호 ~ 5: 노포 선호)",
    4: "주차, 예약 가능 여부, 웨이팅을 얼마나 중요하게 생각하시나요? (0: 상관없음 ~ 5: 매우 중요)",
    5: "매운 음식을 얼마나 좋아하시나요? (0: 안 좋아함 ~ 5: 매우 좋아함)",
    6: "어린이 편의시설이 있는 곳을 선호하시나요? (0: 필요 없음 ~ 5: 매우 중요)",
    7: "식당을 선택할 때 가성비를 얼마나 중요하게 생각하시나요? (0: 중요하지 않음 ~ 5: 매우 중요)"
}

for q_num, question in questions.items():
    if q_num == 1:
        print(question)
        for tag in question_tag_map[q_num]:
            while True:
                try:
                    user_input = input(f"   {tag}: ").strip()
                    score = int(user_input) if user_input else 0
                    if score < 0 or score > 5:
                        raise ValueError
                    question_tag_map[q_num][tag] = score
                    break
                except ValueError:
                    print("⚠️ 0에서 5 사이의 숫자를 입력해주세요!")

    elif q_num == 2:
        print(question)
        available_choices = ["데이트", "혼밥", "가족식사", "주점"]
        selected_tags = []

        for rank, score in [("1순위", 5), ("2순위", 3)]:
            while True:
                try:
                    print("   ".join([f"{i + 1}: {tag}" for i, tag in enumerate(available_choices)]))
                    user_input = input(f"   {rank} 선택 (번호 입력): ").strip()
                    choice = int(user_input) - 1

                    if choice < 0 or choice >= len(available_choices):
                        raise ValueError

                    selected_tag = available_choices.pop(choice)
                    question_tag_map[q_num][selected_tag] = score
                    selected_tags.append(selected_tag)
                    break
                except (ValueError, IndexError):
                    print("⚠️ 올바른 번호를 입력해주세요!")

    elif q_num == 3:
        while True:
            try:
                user_input = input(f"{question} (0~5, Enter 입력 시 기본값 0): ").strip()
                score = int(user_input) if user_input else 0
                if score < 0 or score > 5:
                    raise ValueError
                question_tag_map[q_num]["노포"] = score
                question_tag_map[q_num]["신식"] = 5 - score
                break
            except ValueError:
                print("⚠️ 0에서 5 사이의 숫자를 입력해주세요!")

    elif q_num == 5:
        while True:
            try:
                user_input = input(f"{question} (0~5, Enter 입력 시 기본값 0): ").strip()
                score = int(user_input) if user_input else 0
                if score < 0 or score > 5:
                    raise ValueError
                user_responses[q_num] = (score / 2.5) - 1  # [-1, 1] 범위로 변환
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
                user_responses[q_num] = score / 5
                break
            except ValueError:
                print("⚠️ 0에서 5 사이의 숫자를 입력해주세요!")

tag_weights = {tag: 0 for tag in tags}

for question, score in user_responses.items():
    for tag in question_tag_map.get(question, {}):
        tag_weights[tag] += score

for q_num in [1, 2, 3]:
    for tag, score in question_tag_map[q_num].items():
        tag_weights[tag] += score / 5

child_facility_score = user_responses.get(6, 0)
family_meal_score = question_tag_map[2].get("가족식사", 0)

tag_weights["규모"] += (child_facility_score + family_meal_score) / 10

print("\n사용자 선호도 기반 태그 가중치:")
for tag, weight in tag_weights.items():
    print(f"{tag}: {weight:.2f}")