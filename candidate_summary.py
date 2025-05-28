import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API 키 설정
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_summary(candidate_list):
    prompt = ""
    for c in candidate_list:
        prompt += f"{c['name']} 후보의 선거 공약을 요약해줘.\n"
    
    model = genai.GenerativeModel('gemini-1.5-flash-001')
    response = model.generate_content(prompt)
    return response.text.strip()