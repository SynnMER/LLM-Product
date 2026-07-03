import os

from fastapi import APIRouter, UploadFile, File

from app.services.pdf_service import extract_text_from_pdf
from app.services.ollama_service import OllamaService
from app.services.shared import vector_service
from app.services.pdf_chunks import split_text

from datetime import datetime

router = APIRouter()

ollama = OllamaService()


@router.post("/pdf-analysis")
async def pdf_analysis(file: UploadFile = File(...)):
    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = extract_text_from_pdf(file_path)

    chunks = split_text(text)

    collection_name = file.filename.replace(".", "_")

    for chunk in chunks:
        vector_service.save_chunk(
            chunk,
            file.filename,
            collection_name
        )
    print("TEXT LENGTH:", len(text))
    preview = "\n".join(chunks[:3])
    summary = ollama.generate(
        f"""
    Сделай краткое содержание документа.

    Документ:

    {preview}
    """
    )

    keywords = ollama.generate(
        f"""
    Выдели 5 ключевых слов документа.

    Верни только список через запятую.

    Документ:

    {preview}
    """
    )

    return {
        "summary": summary,
        "keywords": keywords,
        "chunks_saved": len(chunks),
        "collection": collection_name,
        "characters": len(text),
        "pages": text.count("\f") + 1,
        "upload_date": datetime.now().strftime(
            "%d.%m.%Y %H:%M"
        )
    }
