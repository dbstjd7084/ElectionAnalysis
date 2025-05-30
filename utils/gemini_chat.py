import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_response(candidate_name: str, prompt: str, context: str = "") -> str:
    model = genai.GenerativeModel("gemini-1.5-flash-001")
    chat = model.start_chat()
    PROMPT_TEMPLATE = f"""
아래는 대선 후보자의 주요 발언·공약 및 토론 내용입니다.
--------
{context}
--------
{candidate_name} 후보자가 된 것처럼 질문에 답해주세요. 가능하다면 말투도 따라해주세요:

질문: {prompt}

답변(친절하고 이해하기 쉽게):
"""
    if context:
        full_prompt = PROMPT_TEMPLATE.format(context=context, prompt=prompt)
    else:
        full_prompt = prompt
    response = chat.send_message(full_prompt)
    return response.text
