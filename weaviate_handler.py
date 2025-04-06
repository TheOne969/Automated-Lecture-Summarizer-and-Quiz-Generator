# weaviate_handler.py
import weaviate
import weaviate.classes as wvc

class WeaviateHandler:
    def __init__(self, collection_name: str):
        self.client = weaviate.connect_to_local()
        self.collection_name = collection_name

        if self.collection_name not in self.client.collections.list_all():
            self.client.collections.create(
                name=self.collection_name,
                vectorizer_config=wvc.config.Configure.Vectorizer.none(),
                vector_index_config=wvc.config.Configure.VectorIndex.hnsw(),
                properties=[
                    wvc.config.Property(name="text", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="page", data_type=wvc.config.DataType.INT),
                    wvc.config.Property(name="chunk_index", data_type=wvc.config.DataType.INT),
                    wvc.config.Property(name="file_name", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="section", data_type=wvc.config.DataType.TEXT),
                ]
            )

        self.collection = self.client.collections.get(self.collection_name)

    def insert_chunks(self, chunks: list[str], embeddings: list[list[float]], metadatas: list[dict]):
        for chunk, vector, metadata in zip(chunks, embeddings, metadatas):
            self.collection.data.insert(
                properties={**metadata, "text": chunk},
                vector=vector
            )
        print(f"✅ Inserted {len(chunks)} chunks into Weaviate!")
    

    def close(self):
        self.client.close()
