def get_naver_news_smart(candidate_name, candidate_party, candidate_num, max_results=5):
    import os
    import requests
    from datetime import datetime, timedelta, timezone

    client_id = os.getenv("Naver_client_id")
    client_secret = os.getenv("Naver_client_secret")
    today = datetime.now(timezone.utc)
    month_ago = today - timedelta(days=30)

    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }

    # 쿼리
    query = f"대통령 {candidate_name} {candidate_party} 기호 {candidate_num}번 최근"

    params = {
        "query": query,
        "display": max_results,
        "start": 1,
        "sort": "date",
    }
    res = requests.get(url, headers=headers, params=params)
    data = res.json()
    news_list = []
    for item in data.get("items", []):
        pubdate = datetime.strptime(item["pubDate"], "%a, %d %b %Y %H:%M:%S %z")
        if pubdate >= month_ago:
            news_list.append({
                "title": item["title"].replace("<b>", "").replace("</b>", ""),
                "description": item["description"].replace("<b>", "").replace("</b>", ""),
                "date": pubdate.strftime("%Y-%m-%d"),
                "link": item.get("originallink") or item.get("link", "")
            })
    if news_list:  # 기사가 있으면 바로 반환
        return news_list
    return []
