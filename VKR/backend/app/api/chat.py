from fastapi import APIRouter

from app.schemas.chat_schema import QuestionRequest
from app.services.rag_service import RAGService

router = APIRouter()

rag = RAGService()


@router.post("/ask")
def ask_question(request: QuestionRequest):
    
    answer = rag.ask(
        request.question,
        request.collection
    )

    return {
        "question": request.question,
        "answer": answer
    }