from fastapi import APIRouter

from app.schemas.review_schema import ReviewRequest
from app.services.ollama_service import OllamaService
from app.services.shared import vector_service

router = APIRouter()

ollama = OllamaService()


@router.post("/review-analysis")
def review_analysis(request: ReviewRequest):
    prompt = f"""
    Ты эксперт по анализу клиентских отзывов.

    Отзыв:

    {request.text}
    
    Ответь ТОЛЬКО на русском языке.

    Никогда не используй английский язык.

    Все значения JSON должны быть на русском языке.

    Определи:

    1. Тональность отзыва
    2. Основные проблемы
    3. Рекомендации компании

    Верни ТОЛЬКО JSON.

    Пример:

    {{
      "Оценка": "Отрицательный",
      "Проблемы": [
        "долгая доставка"
      ],
      "Рекомендации": [
        "сократить сроки доставки"
      ]
    }}
    
    Оценка может быть только:
    - Позитивный
    - Нейтральный
    - Негативный
    
    Если отзыв позитивный, все равно сформируй минимум 2 рекомендации по поддержанию качества сервиса.

    Никакого текста до JSON и после JSON.
    """
    collection_name = "reviews"

    vector_service.save_chunk(
        request.text,
        "review",
        collection_name
    )

    result = ollama.generate(prompt)

    return {
        "analysis": result
    }