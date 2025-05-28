# news_api.py
import requests
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

# 네이버 API 키 (본인 키로 교체)
Naver_client_id = os.getenv("Naver_client_id")
Naver_client_secret = os.getenv("Naver_client_secret")

def Naver_API(query, wanted_row=5):
    query = requests.utils.quote(query)
    display = wanted_row
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display}&start=1&sort=sim"
    headers = {
        "X-Naver-Client-Id": Naver_client_id,
        "X-Naver-Client-Secret": Naver_client_secret
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        items = json.loads(response.text).get('items', [])
        df = pd.DataFrame(columns=['Title', 'Link', 'Description', 'Content'])
        for i, item in enumerate(items):
            link = item['link']
            title = clean_html_tags(item['title'])
            description = clean_html_tags(item['description'])
            content = get_page_text(link)
            df.loc[i] = [title, link, description, content]
        return df
    except Exception as e:
        print(f"뉴스 검색 실패: {e}")
        return pd.DataFrame()

def get_page_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        paragraphs = soup.find_all('p')
        filtered = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) >= 100]
        text = '\n'.join(filtered)
        return text.strip()[:300]
    except Exception as e:
        return f"크롤링 실패: {e}"

def clean_html_tags(text):
    return re.sub(r'<.*?>', '', text)