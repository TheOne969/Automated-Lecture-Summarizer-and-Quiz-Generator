# test_rag.py
from rag import RAGRetriever
from dotenv import load_dotenv
import os

load_dotenv()
hf_token = os.getenv("HUGGINGFACE_API_KEY")

retriever = RAGRetriever(collection_name="LectureSlides", hf_token=hf_token)

query = "What is the main topic of the lecture?"
top_chunks = retriever.retrieve(query, k=3)

retriever.close()  # ✅ This prevents memory leaks

print("\n🔍 Top Retrieved Chunks:\n")
for i, chunk in enumerate(top_chunks, 1):
    print(f"[{i}] {chunk[:300]}...\n")  # print only first 300 chars
