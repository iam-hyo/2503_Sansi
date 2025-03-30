import numpy as np

# 태그 리스트
tags = ['데이트', '혼밥', '가족식사', '노포', '주점', '양식', '일식', '중식', '분식', '한식',
        '주차', '아동편의시설', '신식', '규모', '예약여부', '웨이팅', '매운정도', '가성비', '거리']

# 질문-태그 매핑
question_tag_map = {
    1: {"양식": 0, "중식": 0, "일식": 0, "분식": 0, "한식": 0},  
    2: {"데이트": 0, "혼밥": 0, "가족식사": 0, "주점": 0},
    3: {"노포": 0, "신식": 0},
    4: {"주차": 0, "예약여부": 0, "웨이팅": 0},  
    5: {"매운정도": 0},
    6: {"아동편의시설": 0, "가족식사": 0},
    7: {"가성비": 0},
    8: {"거리": 0}  # 추가된 질문
}

questions = {
    1: "각 음식 종류별로 선호도를 입력해주세요.\n   (0: 관심 없음 ~ 5: 매우 선호)",
    2: "가장 부합하는 식사 목적을 1순위와 2순위로 선택해주세요.\n   ① 데이트 ② 혼밥 ③ 가족 식사 ④ 술자리(주점)",
    3: "전통 있는 ‘노포(老舗)’와 현대적인 ‘신식’ 레스토랑 중 어디가 더 끌리시나요?\n   (0: 신식 선호 ~ 5: 노포 선호)",
    4: "다음 항목에 대한 중요도를 입력해주세요. (0: 상관없음 ~ 5: 매우 중요)",
    5: "매운 음식을 얼마나 좋아하시나요? (0: 안 좋아함 ~ 5: 매우 좋아함)",
    6: "어린이 편의시설이 있는 곳을 선호하시나요? (0: 필요 없음 ~ 5: 매우 중요)",
    7: "식당을 선택할 때 가성비를 얼마나 중요하게 생각하시나요? (0: 중요하지 않음 ~ 5: 매우 중요)",
    8: "식당을 선택할 때 거리를 얼마나 고려하시나요? (0: 1km도 괜찮다 ~ 5: 가까운 곳이 좋다)"
}

# 사용자 입력 받기
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
                    question_tag_map[q_num][tag] = score / 5  # ✅ [0,1] 범위로 정규화
                    break
                except ValueError:
                    print("⚠️ 0에서 5 사이의 숫자를 입력해주세요!")

    elif q_num == 2:
        print(question)
        available_choices = ["데이트", "혼밥", "가족식사", "주점"]
        selected_tags = []

        for rank, score in [("1순위", 1), ("2순위", 0.6)]:
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
                question_tag_map[q_num]["노포"] = score / 5  # ✅ 정규화
                question_tag_map[q_num]["신식"] = (5 - score) / 5  # ✅ 합이 1 되도록 정규화
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
                question_tag_map[q_num]["매운정도"] = (score / 5) - 1  # ✅ [-1,0] 정규화
                break
            except ValueError:
                print("⚠️ 0에서 5 사이의 숫자를 입력해주세요!")
    elif q_num == 4:
        print(question)
        for tag in ["주차", "예약여부", "웨이팅"]:
            while True:
                try:
                    user_input = input(f"   {tag} (0~5, Enter 입력 시 기본값 0): ").strip()
                    score = int(user_input) if user_input else 0
                    if score < 0 or score > 5:
                        raise ValueError
                    question_tag_map[q_num][tag] = score / 5  # 정규화
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
                question_tag_map[q_num][list(question_tag_map[q_num].keys())[0]] = score / 5  # ✅ [0,1] 정규화
                break
            except ValueError:
                print("⚠️ 0에서 5 사이의 숫자를 입력해주세요!")

# 가중치 계산 함수
def get_user_weights():
    """사용자의 답변을 바탕으로 태그 가중치를 계산하여 반환"""
    tag_weights = {tag: 0 for tag in tags}

    for q_num in question_tag_map:
        for tag, score in question_tag_map[q_num].items():
            tag_weights[tag] += score

    # 가족식사와 아동편의시설 반영하여 규모 점수 조정
    child_facility_score = question_tag_map[6].get("아동편의시설", 0)
    family_meal_score = question_tag_map[2].get("가족식사", 0)
    tag_weights["규모"] += (child_facility_score + family_meal_score) / 10

    return tag_weights

# 최종 가중치 계산
tag_weights = get_user_weights()

# 출력
print("\n✅ 사용자 선호도 기반 태그 가중치:")
for tag, weight in tag_weights.items():
    print(f"{tag}: {weight:.2f}")
    # print(tag_weights)
