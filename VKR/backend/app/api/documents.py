from fastapi import APIRouter

from app.services.shared import vector_service

router = APIRouter()


@router.get("/documents")
def get_documents():

    collections = (
        vector_service.client
        .get_collections()
    )

    return {
        "documents": [
            c.name
            for c in collections.collections
        ]
    }

@router.delete("/documents/{name}")
def delete_document(name: str):

    vector_service.client.delete_collection(
        collection_name=name
    )

    return {
        "message": f"{name} deleted"
    }