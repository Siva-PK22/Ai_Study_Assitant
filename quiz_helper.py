import ast
from together import Together

# Replace with your actual Together AI API key
together = Together(api_key="d65dcd110ef38d53fec06b4bef28afe1f4dfc3ddd20bb212749763deb5f4663e")

def generate_quiz(topic):
    prompt = f"""
    Generate 3 interactive multiple-choice quiz questions on the topic: {topic}.
    Format the response as a JSON list of dictionaries with this structure:
    [
        {{
            "question": "What is ...?",
            "options": ["a", "b", "c", "d"],
            "answer": "a"
        }}
    ]
    Ensure all questions have exactly 4 unique options and one correct answer.
    """

    response = together.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    try:
        content = response.choices[0].message.content.strip()
        quiz_data = ast.literal_eval(content)
        if not isinstance(quiz_data, list):
            raise ValueError("Quiz data is not a list")
        for q in quiz_data:
            if not all(key in q for key in ("question", "options", "answer")):
                raise ValueError("Missing keys in quiz data")
        return quiz_data
    except Exception as e:
        return [{"error": str(e)}]
