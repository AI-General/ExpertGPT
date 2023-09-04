from qdrant_client import QdrantClient
from models.databases.repository import Repository


class Data():
    def __init__(self, qdrant_client:QdrantClient):
        self.db: QdrantClient = qdrant_client

    # def set_file_vectors_ids(self, file_sha1):
    #     response = (
    #         self.db.table("vectors")
    #         .select("id")
    #         .filter("metadata->>file_sha1", "eq", file_sha1)
    #         .execute()
    #     )
    #     return response.data

    # def get_brain_vectors_by_brain_id_and_file_sha1(self, brain_id, file_sha1):
    #     self.set_file_vectors_ids(file_sha1)
    #     # Check if file exists in that brain
    #     response = (
    #         self.db.table("brains_vectors")
    #         .select("brain_id, vector_id")
    #         .filter("brain_id", "eq", brain_id)
    #         .filter("file_sha1", "eq", file_sha1)
    #         .execute()
    #     )

    #     return response

    def upload_records(self, records):
        self.db.upload_records(
            collection_name="vectors",
            records=records
        )
