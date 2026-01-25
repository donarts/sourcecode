

# python -m pip install kss spacy langdetect sentence-transformers umap-learn hdbscan
# python -m spacy download en_core_web_sm

import json
import numpy as np
from langdetect import detect, DetectorFactory
from kss import split_sentences as split_ko
import spacy
from sentence_transformers import SentenceTransformer
import umap
import hdbscan

# 2	자잘한 클러스터 폭증
# 5	적당 (추천 시작점)
# 10	큰 주제만 남음
min_cluster_size = 5
min_samples = min_cluster_size // 2

# -----------------------------------
# 0. 초기 설정
# -----------------------------------

DetectorFactory.seed = 42  # langdetect 재현성
nlp_en = spacy.load("en_core_web_sm")

model = SentenceTransformer(
    "paraphrase-multilingual-mpnet-base-v2"
)

# -----------------------------------
# 1. 언어별 문장 분리 함수
# -----------------------------------

def split_english(text: str):
    doc = nlp_en(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

def split_korean(text: str):
    try:
        # mecab이 있으면 사용
        return split_ko(text, backend="mecab", strip=True)
    except ImportError:
        # 없으면 기본 backend로 fallback
        return split_ko(text, strip=True)

def split_sentences_auto(text: str):
    """
    언어 감지 후 자동 분기
    """
    try:
        lang = detect(text)
    except Exception:
        return [text]

    if lang == "ko":
        sents = split_korean(text)
    elif lang == "en":
        sents = split_english(text)
    else:
        # 기타 언어 or 짧은 텍스트
        sents = [text]

    return sents if sents else [text]

# -----------------------------------
# 2. JSONL 로드 + 문장 분리
# -----------------------------------

documents = []    # 문장 리스트
raw_texts = []    # 원문

with open("input.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        # ✅ 빈 줄 무시
        if not line:
            continue
            
        obj = json.loads(line)
        text = obj["input"].strip()

        raw_texts.append(text)
        sentences = split_sentences_auto(text)
        documents.append(sentences)

# -----------------------------------
# 3. Sentence-BERT 문장 임베딩
# -----------------------------------

doc_embeddings = []

for sentences in documents:
    sent_embeddings = model.encode(
        sentences,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # ✅ 문단 임베딩 = 문장 평균
    doc_embedding = sent_embeddings.mean(axis=0)
    doc_embeddings.append(doc_embedding)

doc_embeddings = np.vstack(doc_embeddings)

# -----------------------------------
# 4. UMAP 차원 축소
# -----------------------------------

umap_embeddings = umap.UMAP(
    n_neighbors=15,
    n_components=5,
    metric="cosine",
    random_state=42
).fit_transform(doc_embeddings)

# -----------------------------------
# 5. HDBSCAN 클러스터링
# -----------------------------------

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=min_cluster_size,
    min_samples=min_samples,
    metric="euclidean"
)

labels = clusterer.fit_predict(umap_embeddings)

# -----------------------------------
# 6. 결과 출력
# -----------------------------------

for i, label in enumerate(labels):
    print(f"[클러스터 {label}] {raw_texts[i]}")


from collections import defaultdict

# 클러스터별로 묶기
clustered = defaultdict(list)

for text, label in zip(raw_texts, labels):
    clustered[label].append(text)

# 결과 출력
for label in sorted(clustered.keys()):
    if label == -1:
        print("\n[Noise / Outlier]")
    else:
        print(f"\n[클러스터 {label}] ({len(clustered[label])}개)")

    for t in clustered[label]:
        print(f"- {t}")
        
# -----------------------------------
# 7. 결과 JSONL 저장
# -----------------------------------

with open("result.jsonl", "w", encoding="utf-8") as f:
    for i, label in enumerate(labels):
        out = {
            "input": raw_texts[i],
            "cluster_id": int(label)
        }
        f.write(json.dumps(out, ensure_ascii=False) + "\n")
