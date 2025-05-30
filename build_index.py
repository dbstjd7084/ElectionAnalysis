# build_index.py

import os
import faiss
import numpy as np
import google.generativeai as genai

# 환경 변수에서 Gemini API 키 읽기
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 후보자 한글 → 영문 매핑 (임의로 작성, 필요시 수정)
NAME_MAP = {
    "이재명": "leejaemyung",
    "김문수": "kimmoonsoo",
    "이준석": "leejoonseok",
    "권영국": "kwonyoungguk",
    "황교안": "hwanggyoan",
    "송진호": "songjinho"
}

def get_embedding(text):
    """text-embedding-004 사용, 768차원 반환"""
    # Google Gemini text-embedding-004 모델 호출
    res = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"
    )
    return np.array(res["embedding"], dtype=np.float32)

def build_faiss_for_candidate(candidate_name):
    folder = f"data/{candidate_name}"
    txt_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.txt')]

    docs = []
    doc_ids = []
    for txt_path in txt_files:
        with open(txt_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    docs.append(line)
                    doc_ids.append(f"{os.path.basename(txt_path)}|{len(doc_ids)}")

    if not docs:
        print(f"{candidate_name}: 임베딩할 문서 없음!")
        return

    embeddings = np.stack([get_embedding(doc) for doc in docs])
    print(f"[{candidate_name}] 임베딩 shape:", embeddings.shape)

    # 영문 이름으로 경로 지정
    eng_name = NAME_MAP[candidate_name]
    os.makedirs("embeddings/faiss", exist_ok=True)
    index_path = f"embeddings/faiss/{eng_name}.index"
    ids_path = f"embeddings/faiss/{eng_name}_ids.npy"

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, index_path)
    print(f"FAISS 인덱스 저장: {index_path}")

    np.save(ids_path, np.array(doc_ids, dtype=object))
    print(f"ID 배열 저장: {ids_path}")

if __name__ == "__main__":
    for candidate in NAME_MAP.keys():
        print(f"=== {candidate} 인덱스 생성 ===")
        build_faiss_for_candidate(candidate)
