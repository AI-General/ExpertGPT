from logger import get_logger
from models.databases.qdrant import (
    Vector_qdrant, Data
)

logger = get_logger(__name__)


class QdrantDB(
    Vector_qdrant, Data
):
    def __init__(self, qdrant_client):
        self.db = qdrant_client
        Vector_qdrant.__init__(self, qdrant_client)
        Data.__init__(self, qdrant_client)

