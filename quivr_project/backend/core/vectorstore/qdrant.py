from typing import Any, List, Optional, Callable

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

class CustomQdrantVectorStore(Qdrant):
    """A custom vector store that uses the match_vectors table instead of the vectors table."""

    brain_id: str = "none"
    encoder = SentenceTransformer('all-MiniLM-L6-v2') 

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
        embeddings: OpenAIEmbeddings,
        encoder: SentenceTransformer,
        content_payload_key: str = "content",
        brain_id: str = "none",
        # embedding_function: Optional[Callable] = None
    ):
        super().__init__(client=client, collection_name=collection_name, content_payload_key=content_payload_key, embeddings=embeddings)
        self.brain_id = brain_id
        self.encoder = encoder

    def similarity_search(
        self,
        query: str,
        k: int = 6,
        threshold: float = 0.5,
        **kwargs: Any
    ) -> List[Document]:
        """
        self,
        query: str,
        k: int = 4,
        filter: Optional[MetadataFilter] = None,
        search_params: Optional[common_types.SearchParams] = None,
        offset: int = 0,
        score_threshold: Optional[float] = None,
        consistency: Optional[common_types.ReadConsistency] = None,
        **kwargs: Any,
        """
        # vectors = self._embeddings_function(query)
        query_vector=self.encoder.encode(query).tolist()
        # query_embedding = vectors

        res = self.client.search(
            collection_name=self.collection_name,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="brain_id",
                        match=models.MatchValue(
                            value=self.brain_id,
                        ),
                    )
                ]
            ),
            search_params=models.SearchParams(
                hnsw_ef=128,
                exact=False
            ),
            with_payload=[self.content_payload_key],
            query_vector=query_vector,
            limit=k,
        )

        match_result = [
            (
                Document(
                    metadata=search.get("metadata", {}),  # type: ignore
                    page_content=search.get("content", ""),
                ),
                search.get("similarity", 0.0),
            )
            for search in res.data
            if search.get("content")
        ]

        documents = [doc for doc, _ in match_result]
        print("####################################################################")
        print(documents)

        return documents


