import numpy as np

tags = ['데이트', '혼밥', '가족식사', '노포', '주점', '양식', '일식', '중식', '분식', '한식',
        '주차', '예약여부', '웨이팅', '매운정도', '가성비', '아동편의시설', '규모', '신식']

question_tag_map = {
    1: {"양식": 0, "중식": 0, "일식": 0, "분식": 0, "한식": 0},  
    2: {"데이트": 0, "혼밥": 0, "가족식사": 0, "주점": 0},
    3: {"노포": 0, "신식": 0},
    4: {"주차": 1},
    5: {"예약여부": 1},
    6: {"웨이팅": 1},
    7: {"매운정도": 1},
    8: {"아동편의시설": 1, "가족식사": 1},
    9: {"가성비": 1},
}

def normalize(value, min_val, max_val, new_min, new_max):
    return new_min + (value - min_val) * (new_max - new_min) / (max_val - min_val)

def get_user_weights():
    tag_weights = {tag: 0 for tag in tags}
    user_responses = {}
    
    # 1번 문항: 음식 종류 선호도
    print("각 음식 종류별로 선호도를 입력해주세요. (1순위: 5점, 2순위: 3점)")
    available_choices = list(question_tag_map[1].keys())
    selected_tags = []
    for rank, score in [("1순위", 5), ("2순위", 3)]:
        while True:
            print("   ".join([f"{i + 1}: {tag}" for i, tag in enumerate(available_choices)]))
            user_input = input(f"   {rank} 선택 (번호 입력): ").strip()
            try:
                choice = int(user_input) - 1
                if choice < 0 or choice >= len(available_choices):
                    raise ValueError
                selected_tag = available_choices.pop(choice)
                question_tag_map[1][selected_tag] = score / 5
                selected_tags.append(selected_tag)
                break
            except (ValueError, IndexError):
                print("⚠️ 올바른 번호를 입력해주세요!")
    
    # 2~9번 문항 입력 받기
    questions = {
        2: "가장 부합하는 식사 목적을 선택하세요. (1순위: 5점, 2순위: 3점)",
        3: "노포 vs 신식 선호도 (0: 신식 ~ 5: 노포)",
        4: "주차가 가능한 곳을 선호하시나요? (0~5)",
        5: "예약이 가능한 곳을 선호하시나요? (0~5)",
        6: "웨이팅(줄 서기)을 감수할 수 있나요? (0~5)",
        7: "매운 음식을 얼마나 좋아하시나요? (0~5)",
        8: "어린이 편의시설이 있는 곳을 선호하시나요? (0~5)",
        9: "식당을 선택할 때 가성비를 얼마나 중요하게 생각하시나요? (0~5)",
    }
    
    for q_num, question in questions.items():
        while True:
            try:
                user_input = input(f"{question}: ").strip()
                score = int(user_input) if user_input else 0
                if score < 0 or score > 5:
                    raise ValueError
                
                if q_num == 3:  # 노포 vs 신식
                    question_tag_map[q_num]["노포"] = score / 5
                    question_tag_map[q_num]["신식"] = (5 - score) / 5
                elif q_num == 6 or q_num == 7:  # 웨이팅, 매운정도 정규화 (-1 ~ 1)
                    user_responses[q_num] = normalize(score, 0, 5, -1, 1)
                else:
                    user_responses[q_num] = score / 5
                break
            except ValueError:
                print("⚠️ 0에서 5 사이의 숫자를 입력해주세요!")
    
    # 태그 가중치 반영
    for question, score in user_responses.items():
        for tag in question_tag_map.get(question, {}):
            tag_weights[tag] += score
    
    for q_num in [1, 2]:
        for tag, score in question_tag_map[q_num].items():
            tag_weights[tag] += score
    
    # 규모 태그 계산
    child_facility_score = user_responses.get(8, 0)
    family_meal_score = question_tag_map[2].get("가족식사", 0)
    tag_weights["규모"] += (child_facility_score + family_meal_score * 5) / 10
    
    return tag_weights

if __name__ == "__main__":
    user_weights = get_user_weights()
    print("\n사용자 선호도 기반 태그 가중치:")
    for tag, weight in user_weights.items():
        print(f"{tag}: {weight:.2f}")
