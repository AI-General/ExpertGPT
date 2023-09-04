from qdrant_client import QdrantClient
from qdrant_client.http import models
from models.databases.repository import Repository


class Vector_qdrant():
    def __init__(self, qdrant_client:QdrantClient):
        self.db: QdrantClient = qdrant_client

    def get_payloads_data_sha1(self, data_sha1):
        response = self.db.scroll(
            collection_name="vectors",
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="data_sha1",
                        match=models.MatchValue(value=data_sha1),
                    )
                ]
            ),
        )
        return response
    
    def delete_vectors_from_brain(self, data_sha1):
        response = self.db.delete(
            collection_name="vectors",
                points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="data_sha1",
                            match=models.MatchValue(value=data_sha1),
                        ),
                    ],
                )
            ),
        )
        return response
