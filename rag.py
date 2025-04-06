# rag.py
from typing import List
import weaviate.classes as wvc
from weaviate_handler import WeaviateHandler

class RAGRetriever:
    def __init__(self, collection_name: str, embedding_model):
        """
        :param collection_name: name of the Weaviate collection
        :param embedding_model: model with an .encode(list[str], convert_to_numpy=True) -> np.ndarray
        """
        self.embedding_model = embedding_model
        self.weaviate_handler = WeaviateHandler(collection_name)

    def retrieve(self, query: str, k: int = 5) -> List[str]:
        # 1) Embed the query
        vector = self.embedding_model.encode([query], convert_to_numpy=True)[0].tolist()
        # 2) Perform the vector search
        collection = self.weaviate_handler.collection
        response = collection.query.near_vector(
            near_vector=vector,
            limit=k,
            return_properties=["text"],
            return_metadata=wvc.query.MetadataQuery(distance=True)
        )
        # 3) Return the text
        return [obj.properties["text"] for obj in response.objects]

    def close(self):
        """Close the underlying Weaviate client."""
        self.weaviate_handler.client.close()
