import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from report_generator import (
    create_review_report,
    create_document_report
)
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
import json

from api import (
    analyze_review,
    upload_pdf,
    ask_document,
    get_documents,
    delete_document
)
if "question" not in st.session_state:
    st.session_state.question = ""

if "chat_answer" not in st.session_state:
    st.session_state.chat_answer = None

st.set_page_config(
    page_title="LLM Analytics Platform",
    layout="wide"
)

if "review_history" not in st.session_state:
    st.session_state.review_history = []

if "documents_history" not in st.session_state:
    st.session_state.documents_history = []

if "review_text" not in st.session_state:
    st.session_state.review_text = ""

if "review_result" not in st.session_state:
    st.session_state.review_result = None

if "pdf_result" not in st.session_state:
    st.session_state.pdf_result = None

if "collection" not in st.session_state:
    st.session_state.collection = ""

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}

if "reviews_count" not in st.session_state:
    st.session_state.reviews_count = 0

if "positive_count" not in st.session_state:
    st.session_state.positive_count = 0

if "negative_count" not in st.session_state:
    st.session_state.negative_count = 0

if "neutral_count" not in st.session_state:
    st.session_state.neutral_count = 0



st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI';
}

.main {
    padding-top: 1rem;
}

h1 {
    color: #2563eb;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-weight: 600;
}

.result-card {
    padding: 15px;
    border-radius: 12px;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    margin-bottom: 10px;
}

.sentiment-positive {
    color: #16a34a;
    font-size: 28px;
    font-weight: bold;
}

.sentiment-negative {
    color: #dc2626;
    font-size: 28px;
    font-weight: bold;
}

.sentiment-neutral {
    color: #f59e0b;
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

st.title("🤖 Аналитическая платформа LLM")

st.write(
    "Система анализа отзывов и документов"
)

try:

    docs = get_documents()["documents"]

    documents_count = len(docs)

except:

    documents_count = 0

questions_count = sum(
    len(history)
    for history in st.session_state.chat_sessions.values()
)

reviews_count = (
    st.session_state.reviews_count
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📄 Документы",
        documents_count
    )

with col2:
    st.metric(
        "💬 Сообщения",
        questions_count
    )

with col3:
    st.metric(
        "⭐ Отзывы",
        reviews_count
    )

st.divider()

st.subheader("📊 Аналитическая панель")

col1, col2 = st.columns(2)

with col1:

    data = pd.DataFrame(
        {
            "Тип": [
                "Позитивные",
                "Негативные",
                "Нейтральные"
            ],
            "Количество": [
                st.session_state.positive_count,
                st.session_state.negative_count,
                st.session_state.neutral_count
            ]
        }
    )

    st.bar_chart(
        data.set_index("Тип")
    )

with col2:

    fig, ax = plt.subplots()

    values = [
        st.session_state.positive_count,
        st.session_state.negative_count,
        st.session_state.neutral_count
    ]

    if sum(values) > 0:
        ax.pie(
            values,
            labels=[
                "Позитивные",
                "Негативные",
                "Нейтральные"
            ],
            autopct="%1.1f%%"
        )
    else:
        ax.text(
            0.5,
            0.5,
            "Нет данных",
            ha="center",
            va="center"
        )

    st.pyplot(fig)

st.divider()

st.subheader("📈 Сводная статистика")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Позитивные отзывы",
        st.session_state.positive_count
    )

with col2:

    st.metric(
        "Негативные отзывы",
        st.session_state.negative_count
    )

with col3:

    st.metric(
        "Нейтральные отзывы",
        st.session_state.neutral_count
    )

st.divider()

mode = st.sidebar.radio(
    "Выберите режим",
    [
        "Главная",
        "Анализ отзывов",
        "Анализ документов",
        "Чат с документом"
    ]
)
st.sidebar.divider()

st.sidebar.title(
    "📊 Dashboard"
)

st.sidebar.metric(
    "Документы",
    documents_count
)

st.sidebar.metric(
    "Сообщения",
    questions_count
)

st.sidebar.metric(
    "Отзывы",
    reviews_count
)

st.sidebar.divider()

st.sidebar.subheader(
    "📚 Документы"
)

st.sidebar.divider()

try:

    docs = get_documents()["documents"]

    for doc in docs:

        col1, col2 = st.sidebar.columns(
            [4, 1]
        )

        with col1:
            st.sidebar.write(
                f"📄 {doc}"
            )

        with col2:

            if st.button(
                "❌",
                key=f"del_{doc}"
            ):

                delete_document(doc)

                st.rerun()

except:
    pass

# --------------------------
# Главная
# --------------------------

if mode == "Главная":

    st.header(
        "📊 Панель управления"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Документов",
            documents_count
        )

    with col2:
        st.metric(
            "Сообщений",
            questions_count
        )

    with col3:
        st.metric(
            "Отзывов",
            reviews_count
        )

    st.divider()

    col1, col2 = st.columns(2)
    st.subheader(
        "⭐ Оценка системы"
    )
    if "ratings" not in st.session_state:
        st.session_state.ratings = []
    rating = st.slider(
        "Оцените качество ответа",
        1,
        5,
        5
    )

    st.write(
        f"Текущая оценка: {rating}"
    )
    with col1:

        st.subheader(
            "📚 Последние документы"
        )

        try:

            docs = get_documents()["documents"]

            for doc in docs[-5:]:

                st.info(doc)

        except:

            st.warning(
                "Документы отсутствуют"
            )

    with col2:

        st.subheader(
            "📝 Последние отзывы"
        )

        for item in reversed(
            st.session_state.review_history[-5:]
        ):

            st.write(
                f"**{item['sentiment']}**"
            )

            st.caption(
                item["text"]
            )

        st.divider()

        st.subheader(
            "📄 История документов"
        )

        if st.session_state.documents_history:

            docs_df = pd.DataFrame(
                st.session_state.documents_history
            )

            st.dataframe(
                docs_df,
                use_container_width=True
            )
            csv = docs_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📥 Скачать историю документов",
                data=csv,
                file_name="documents_history.csv",
                mime="text/csv"
            )

        else:

            st.info(
                "Документы пока не загружались"
            )
# --------------------------
# Анализ отзывов
# --------------------------

if mode == "Анализ отзывов":

    st.header("Анализ клиентских отзывов")

    review_text = st.text_area(
        "Введите текст отзыва",
        value=st.session_state.review_text,
        height=250
    )

    st.session_state.review_text = review_text

    if st.button("Проанализировать отзыв"):

        if not review_text.strip():
            st.warning("Введите текст отзыва")
        else:

            with st.spinner("Выполняется анализ..."):

                result = analyze_review(review_text)

                if "error" in result:
                    st.error(result["error"])

                else:

                    st.session_state.review_result = result

                    analysis = json.loads(
                        result["analysis"]
                    )

                    sentiment = analysis["Оценка"].lower()

                    st.session_state.reviews_count += 1

                    st.session_state.review_history.append(
                        {
                            "text": review_text[:100],
                            "sentiment": analysis["Оценка"]
                        }
                    )

                    if "позитив" in sentiment:
                        st.session_state.positive_count += 1

                    elif (
                            "негатив" in sentiment
                            or "отрицат" in sentiment
                    ):
                        st.session_state.negative_count += 1

                    else:
                        st.session_state.neutral_count += 1

    if st.session_state.review_result:

        result = st.session_state.review_result

        st.subheader("Результат")

        try:

            analysis = json.loads(
                result["analysis"]
            )

            sentiment = analysis["Оценка"].lower()

            if any(word in sentiment for word in [
                "позитив",
                "positive"
            ]):
                css_class = "sentiment-positive"

            elif any(word in sentiment for word in [
                "негатив",
                "отрицат",
                "negative"
            ]):
                css_class = "sentiment-negative"

            else:
                css_class = "sentiment-neutral"

            st.markdown(
                f"""
                <div class="{css_class}">
                    {analysis["Оценка"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("Проблемы")

            if analysis["Проблемы"]:

                for item in analysis["Проблемы"]:

                    st.markdown(
                        f"""
                        <div class="result-card">
                            ⚠️ {item}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.success("Проблем не обнаружено")

            st.subheader("Рекомендации")

            for item in analysis["Рекомендации"]:

                st.markdown(
                    f"""
                    <div class="result-card">
                        ✅ {item}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            report_file = create_review_report(
                analysis
            )

            with open(
                    report_file,
                    "rb"
            ) as file:

                st.download_button(
                    label="📄 Скачать отчет",
                    data=file,
                    file_name="review_report.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(str(e))
            #st.json(result)


# --------------------------
# Анализ документов
# --------------------------

elif mode == "Анализ документов":

    st.header("Загрузка PDF документа")

    uploaded_file = st.file_uploader(
        "Выберите PDF",
        type=["pdf"]
    )

    if uploaded_file and st.button("Загрузить документ"):

        with st.spinner("Обработка PDF..."):

            result = upload_pdf(uploaded_file)

            st.session_state.pdf_result = result
            st.session_state.collection = result["collection"]

            st.session_state.documents_history.append(
                {
                    "name": uploaded_file.name,
                    "pages": result["pages"],
                    "characters": result["characters"],
                    "date": result["upload_date"]
                }
            )

    if st.session_state.pdf_result:
        result = st.session_state.pdf_result

        st.success(
            "Документ успешно обработан"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Страниц",
                result["pages"]
            )

        with col2:
            st.metric(
                "Символов",
                result["characters"]
            )

        with col3:
            st.metric(
                "Чанков",
                result["chunks_saved"]
            )

        st.write(
            f"Коллекция: {result['collection']}"
        )

        st.write(
            f"Количество чанков: {result['chunks_saved']}"
        )

        st.subheader(
            "Краткое содержание"
        )

        st.write(
            result["summary"]
        )

        st.subheader(
            "🔑 Ключевые слова"
        )

        st.info(
            result["keywords"]
        )

        st.subheader(
            "📋 Паспорт документа"
        )

        st.write(
            f"Дата загрузки: {result['upload_date']}"
        )

        st.write(
            f"Страниц: {result['pages']}"
        )

        st.write(
            f"Символов: {result['characters']}"
        )

        st.write(
            f"Чанков: {result['chunks_saved']}"
        )
        report_file = create_document_report(
            result
        )

        with open(
                report_file,
                "rb"
        ) as file:

            st.download_button(
                label="📄 Скачать паспорт документа",
                data=file,
                file_name="document_report.pdf",
                mime="application/pdf"
            )

        st.session_state[
            "collection"
        ] = result["collection"]


# --------------------------
# Чат с документом
# --------------------------

elif mode == "Чат с документом":

    left, right = st.columns(
        [1, 3]
    )
    with left:

        st.subheader("📚 Документы")

        search_doc = st.text_input(
            "Поиск документа"
        )

        try:

            documents = get_documents()["documents"]

            filtered_docs = [
                doc for doc in documents
                if search_doc.lower() in doc.lower()
            ]

            for doc in filtered_docs:

                if st.button(
                        f"📄 {doc}",
                        key=f"chat_doc_{doc}"
                ):
                    st.session_state.collection = doc

        except:

            st.error(
                "Не удалось загрузить список документов"
            )
        st.divider()

        st.subheader(
            "💬 История вопросов"
        )

        current_doc = st.session_state.collection

        if (
                current_doc
                and current_doc in st.session_state.chat_sessions
        ):

            history = (
                st.session_state.chat_sessions[
                    current_doc
                ]
            )

            user_messages = [
                msg["content"]
                for msg in history
                if msg["role"] == "user"
            ]

            for question in reversed(
                    user_messages[-10:]
            ):
                st.caption(
                    f"📝 {question[:40]}"
                )

    with right:

        collection = st.session_state.collection

        if collection not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[collection] = []

        chat_history = st.session_state.chat_sessions[collection]

        st.header("💬 Чат с документом")

        if st.button(
                "🗑 Очистить чат"
        ):
            chat_history.clear()
            st.rerun()

        if collection:
            st.subheader(
                "📄 Информация о документе"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.info(
                    f"Название: {collection}"
                )

                st.success(
                    "Статус: Загружен"
                )

            with col2:
                st.metric(
                    "Сообщений",
                    len(chat_history)
                )

                st.metric(
                    "Источник",
                    "FAISS"
                )

            st.divider()

        if not collection:
            st.info(
                "Выберите документ слева"
            )
        try:

            documents = get_documents()["documents"]

        except Exception:

            documents = []



        question = st.chat_input(
            "Введите вопрос..."
        )

        if question:
            chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.spinner("Поиск ответа..."):

                result = ask_document(
                    question,
                    collection
                )

                answer = result["answer"]["answer"]

                chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

        for message in chat_history:

            with st.chat_message(
                message["role"]
            ):
                st.write(
                    message["content"]
                )
        chat_text = ""

        for msg in chat_history:
            role = "Пользователь" if msg["role"] == "user" else "Ассистент"

            chat_text += f"{role}:\n"
            chat_text += f"{msg['content']}\n\n"

        st.download_button(
            "📥 Скачать чат",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )