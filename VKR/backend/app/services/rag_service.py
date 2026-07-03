from app.services.shared import vector_service
from app.services.ollama_service import OllamaService


class RAGService:

    def __init__(self):
        self.vector_service = vector_service
        self.ollama = OllamaService()

    def ask(
            self,
            question: str,
            collection_name: str
    ):
        results = self.vector_service.search(
            question=question,
            collection_name=collection_name
        )

        context = "\n\n".join(
            item["text"]
            for item in results
        )

        print("\n===== CONTEXT =====")
        print(context)
        print("===================\n")

        prompt = f"""
Ты отвечаешь только на основе контекста.

Контекст:

{context}

Вопрос:

{question}

Если ответа нет в контексте,
так и скажи.
"""

        return {
            "answer": self.ollama.generate(prompt),
            "sources": list(
                set(
                    item["document"]
                    for item in results
                )
            )
        }