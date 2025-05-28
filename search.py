import urllib.request
import urllib.parse
import json
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

Naver_client_id = 'EVT1QPtNy7sKPMN8PUTA'
Naver_client_secret = 'jMJXBl3MNP' 

def Naver_API(query, wanted_row):
    query = urllib.parse.quote(query)
    display = 100
    start = 1
    end = wanted_row + 1
    sort = 'sim'

    df = pd.DataFrame(columns=['Title', 'Link', 'Description', 'Content'])
    saved_count = 0

    for start_index in range(start, end, display):
        url = f"https://openapi.naver.com/v1/search/webkr?query={query}&display={display}&start={start_index}&sort={sort}"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", Naver_client_id)
        request.add_header("X-Naver-Client-Secret", Naver_client_secret)
        try:
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read()
                items = json.loads(response_body.decode('utf-8'))['items']
                remove_tag = re.compile('<.*?>')
                for item in items:
                    link = item['link']
                    title = re.sub(remove_tag, '', item['title'])
                    description = re.sub(remove_tag, '', item['description'])
                    print(link)
                    content = get_page_text(link)
                    print(content)
                    if content and len(content) >= 100 and not content.startswith("크롤링 실패"):
                        df.loc[saved_count] = [title, link, description, content]
                        saved_count += 1
                        if saved_count >= 2:   # 2개 저장 시 바로 종료
                            return df.reset_index(drop=True)
            else:
                print("Error Code:", rescode)
                return df.reset_index(drop=True)
        except Exception as e:
            print("Exception:", e)
            return df.reset_index(drop=True)
    return df.reset_index(drop=True)

def get_page_text(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        resp = requests.get(url, headers=headers, timeout=7)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        paragraphs = soup.find_all('div')
        filtered = [
            p.get_text(strip=True) 
            for p in paragraphs 
            if len(p.get_text(strip=True)) >= 250
        ]
        text = '\n'.join(filtered)
        return text.strip()
    except Exception as e:
        return f"크롤링 실패: {e}"


import re

def chunk_text(text, chunk_size=1024):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current_chunk = ""
    chunk_id = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        # 1. 아주 긴 문장은 chunk_size 단위로 강제 쪼개기
        while len(sentence) > chunk_size:
            part = sentence[:chunk_size]
            if current_chunk:
                chunks.append({"chunk_id": chunk_id, "text": current_chunk.strip()})
                chunk_id += 1
                current_chunk = ""
            chunks.append({"chunk_id": chunk_id, "text": part})
            chunk_id += 1
            sentence = sentence[chunk_size:]

        # 2. 현재 chunk에 sentence를 더했을 때 chunk_size 넘으면 chunk 분리
        if len(current_chunk) + len(sentence) + 1 > chunk_size:
            if current_chunk:
                chunks.append({"chunk_id": chunk_id, "text": current_chunk.strip()})
                chunk_id += 1
                current_chunk = ""

        # 3. 문장 추가
        if current_chunk:
            current_chunk += " " + sentence
        else:
            current_chunk = sentence

    if current_chunk:
        chunks.append({"chunk_id": chunk_id, "text": current_chunk.strip()})

    return chunks


# ---- Main Workflow ----

# 1. CSV 파일 불러오기
csv_path = "최종_누락된_정보공개서_리스트.csv"   # <- 파일 경로 수정
df_csv = pd.read_csv(csv_path)

import os

results = []

output_dir = "brandNm_jsons"
os.makedirs(output_dir, exist_ok=True)

for idx, row in df_csv.iterrows():
    corpNm = str(row['corpNm'])
    brandNm = str(row['brandNm'])
    # 파일명 안전하게
    safe_brandNm = re.sub(r'[\\/:*?"<>|]', '_', brandNm)
    query = f"{brandNm} {corpNm} 사업 및 기업 정보"
    print(f"\n[{idx+1}/{len(df_csv)}] {query}")

    naver_results = Naver_API(query, 5)
    contents = naver_results['Content'].tolist() if not naver_results.empty else []
    main1 = contents[0] if len(contents) > 0 else ''
    main2 = contents[1] if len(contents) > 1 else ''

    chunked1 = chunk_text(main1, 1024)
    chunked2 = chunk_text(main2, 1024)

    data = {
        "corpNm": corpNm,
        "brandNm": brandNm,
        "본문1": chunked1,
        "본문2": chunked2
    }

    # brandNm별로 json 저장
    json_path = os.path.join(output_dir, f"{safe_brandNm}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    time.sleep(1)

print("brandNm별 JSON 저장 완료!")
