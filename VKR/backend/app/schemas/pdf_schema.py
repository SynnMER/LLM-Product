from pydantic import BaseModel


class PdfResponse(BaseModel):
    summary: str