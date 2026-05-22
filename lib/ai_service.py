import os
import json
from dotenv import load_dotenv
from groq import Groq

# Загружаем переменные окружения из файла .env
load_dotenv()

# Инициализируем клиента Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_resume_groq(resume_text, vacancy_text):
    """
    Sends resume and vacancy data to Groq and returns a high-quality career analysis.
    This function is ready for backend integration.
    """
    
    # Улучшенный системный промпт (Закрывает задачу "Improve quality of suggestions")
    system_instruction = (
        "You are an elite IT Recruiter and Technical Career Coach. Your job is to critically compare "
        "the candidate's resume with the job description and return a deep, actionable analysis in strict JSON format.\n\n"
        "To maximize suggestion quality:\n"
        "- Strong points must highlight exact technical matches and relevant project experience.\n"
        "- Weak points must clearly list missing core stack, missing tools, or gaps in years of experience.\n"
        "- Recommendations must be highly specific, giving actionable advice on exactly what projects or keywords to add.\n\n"
        "The JSON format must look EXACTLY like this with no markdown wrapping:\n"
        "{\n"
        "  \"match_percentage\": 85,\n"
        "  \"strong_points\": [\"Bullet 1\", \"Bullet 2\"],\n"
        "  \"weak_points\": [\"Bullet 1\", \"Bullet 2\"],\n"
        "  \"recommendations\": [\"Specific advice 1\", \"Specific advice 2\"]\n"
        "}\n"
        "Respond strictly in English. Do not include any extra text, backticks (```), or markdown blocks outside the JSON!"
    )

    # Делаем ультрабыстрый запрос к актуальной модели Llama-3.1
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        response_format={ "type": "json_object" }, 
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Resume:\n{resume_text}\n\nJob Description:\n{vacancy_text}"}
        ]
    )

    # Получаем ответ-строку и превращаем в готовый Python-словарь
    result_string = response.choices[0].message.content
    return json.loads(result_string)
