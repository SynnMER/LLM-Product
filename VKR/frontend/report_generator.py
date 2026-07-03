
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_review_report(
        analysis,
        filename="report.pdf"
):

    # Регистрируем русский шрифт
    pdfmetrics.registerFont(
        TTFont(
            "Arial",
            r"C:\Windows\Fonts\arial.ttf"
        )
    )

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    # Назначаем Arial всем стилям
    for style_name in styles.byName:
        styles[style_name].fontName = "Arial"

    elements = []

    elements.append(
        Paragraph(
            "LLM Analytics Platform",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Тональность: {analysis['Оценка']}",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "Проблемы:",
            styles["Heading3"]
        )
    )

    if analysis["Проблемы"]:
        for item in analysis["Проблемы"]:
            elements.append(
                Paragraph(
                    f"• {item}",
                    styles["Normal"]
                )
            )
    else:
        elements.append(
            Paragraph(
                "Проблем не обнаружено",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "Рекомендации:",
            styles["Heading3"]
        )
    )

    for item in analysis["Рекомендации"]:
        elements.append(
            Paragraph(
                f"• {item}",
                styles["Normal"]
            )
        )

    doc.build(elements)

    return filename

def create_document_report(
        document_data,
        filename="document_report.pdf"
):
    pdfmetrics.registerFont(
        TTFont(
            "Arial",
            r"C:\Windows\Fonts\arial.ttf"
        )
    )

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    for style_name in styles.byName:
        styles[style_name].fontName = "Arial"

    elements = []

    elements.append(
        Paragraph(
            "LLM Analytics Platform",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Паспорт документа",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            f"Название: {document_data['collection']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Дата загрузки: {document_data['upload_date']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Страниц: {document_data['pages']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Символов: {document_data['characters']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Чанков: {document_data['chunks_saved']}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "Краткое содержание",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            document_data["summary"],
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "Ключевые слова",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            str(document_data["keywords"]),
            styles["Normal"]
        )
    )

    doc.build(elements)

    return filename