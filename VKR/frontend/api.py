import requests

BASE_URL = "http://127.0.0.1:8000"


def analyze_review(text):
    try:
        response = requests.post(
            f"{BASE_URL}/review-analysis",
            json={"text": text},
            timeout=300
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        return {
            "error": str(e)
        }

def upload_pdf(file):
    files = {
        "file": file
    }

    response = requests.post(
        f"{BASE_URL}/pdf-analysis",
        files=files
    )

    return response.json()


def ask_document(question, collection):
    response = requests.post(
        f"{BASE_URL}/ask",
        json={
            "question": question,
            "collection": collection
        }
    )

    return response.json()

def get_documents():

    response = requests.get(
        f"{BASE_URL}/documents"
    )

    return response.json()

def delete_document(name):

    response = requests.delete(
        f"{BASE_URL}/documents/{name}"
    )

    return response.json()