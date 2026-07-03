from fastapi import FastAPI

from app.api.review import router as review_router
from app.api.pdf import router as pdf_router
from app.api.chat import router as chat_router
from app.api.documents import router as documents_router

app = FastAPI(
    title="LLM Analytics Platform"
)

app.include_router(review_router)
app.include_router(pdf_router)
app.include_router(chat_router)
app.include_router(documents_router)