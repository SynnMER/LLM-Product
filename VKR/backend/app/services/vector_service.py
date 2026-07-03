from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance
)
import uuid


class VectorService:

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.client = QdrantClient(
            path="storage/qdrant"
        )

        self.collection_name = "documents"

        collections = self.client.get_collections()

        names = [c.name for c in collections.collections]

        if self.collection_name not in names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

    def embed(self, text: str):
        return self.model.encode(text).tolist()

    def save_chunk(
            self,
            text: str,
            document: str,
            collection_name: str
    ):
        vector = self.embed(text)

        self.create_collection_if_not_exists(
            collection_name
        )

        self.client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "text": text,
                        "document": document
                    }
                )
            ]
        )

    def create_collection_if_not_exists(self, collection_name: str):

        collections = self.client.get_collections()

        names = [c.name for c in collections.collections]

        if collection_name not in names:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

    def search(
            self,
            question: str,
            collection_name: str,
            limit: int = 3
    ):
        vector = self.embed(question)

        results = self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit
        )

        return [
            {
                "text": item.payload["text"],
                "document": item.payload.get("document")
            }
            for item in results.points
        ]