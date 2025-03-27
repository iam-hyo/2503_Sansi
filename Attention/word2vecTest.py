from sentence_transformers import SentenceTransformer
import numpy as np

# 📌 KoSentenceBERT 모델 로드
model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

# 📌 단어/문장 임베딩 생성
sentences = ["느끼함", "까르보나라", "치즈", "냉면"]
embeddings = model.encode(sentences)

# 📌 임베딩 확인 (차원: 768)
for sentence, embedding in zip(sentences, embeddings):
    print(f"'{sentence}' 임베딩 차원: {embedding.shape}")

# 📌 코사인 유사도 계산 함수
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# 📊 유사도 계산
sim = cosine_similarity(embeddings[0], embeddings[1])  # "똥쟁이" vs "싱크대"
sim2 = cosine_similarity(embeddings[0], embeddings[2])  # "똥쟁이" vs "변기"
sim3 = cosine_similarity(embeddings[0], embeddings[3])  # "똥쟁이" vs "학생회장"

print(f"'{sentences[0]}'과 '{sentences[1]}'의 유사도: {sim:.4f}")
print(f"'{sentences[0]}'과 '{sentences[2]}'의 유사도: {sim2:.4f}")
print(f"'{sentences[0]}'과 '{sentences[3]}'의 유사도: {sim3:.4f}")
