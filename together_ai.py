import requests

TOGETHER_API_KEY = "d65dcd110ef38d53fec06b4bef28afe1f4dfc3ddd20bb212749763deb5f4663e"  # paste your key here
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

def generate_study_material(prompt):
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(TOGETHER_API_URL, headers=HEADERS, json=data)
    return response.json()["choices"][0]["message"]["content"]

def generate_quiz(prompt):
    quiz_prompt = f"Generate a 5-question multiple choice quiz with answers based on this topic:\n\n{prompt}"
    return generate_study_material(quiz_prompt)
