# llm_analyzer.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_titles(query, titles):
    numbered_titles = "\n".join([f"{i+1}. {t['title']}" for i, t in enumerate(titles)])
    prompt = f"""
    You are an assistant helping to find the best YouTube video for the topic: "{query}".
    Here are the video titles:

    {numbered_titles}

    Pick the most relevant one and explain why briefly. Output only the number and reasoning.
    """

    response = model.generate_content(prompt)
    return response.text.strip()
