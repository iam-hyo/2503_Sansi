import numpy as np
from gensim.models import KeyedVectors

# 사전 학습된 Word2Vec 모델 로드 (구글에서 학습된 뉴스 코퍼스)
word_vectors = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)

# 문장 예제
sentence = ["나는", "오늘", "날씨가", "매우", "좋아서", "기분이", "좋다"]

# 한국어는 지원 안 되니 유사한 영어 문장으로 변환
sentence_en = ["I", "feel", "weather", "very", "good", "mood", "happy"]

# 각 단어를 임베딩으로 변환
embeddings = np.array([word_vectors[word] for word in sentence_en])

# 쿼리 정의 (예: "기분이" -> "mood")
query = embeddings[sentence.index("기분이")]

# 어텐션 스코어 계산
scores = np.dot(embeddings, query)
print("어텐션 스코어:", scores)
