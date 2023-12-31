import os
from dotenv import load_dotenv
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

load_dotenv()
qdrant_location = os.getenv("QDRANT_LOCATION")
qdrant_port = os.getenv("QDRANT_PORT")
qdrant = QdrantClient(location=qdrant_location, port=qdrant_port)

try:
    response = qdrant.delete(
        collection_name="vectors",
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                ],
            )
        ),
    )
    print (response)
except Exception as e:
    print(e)
