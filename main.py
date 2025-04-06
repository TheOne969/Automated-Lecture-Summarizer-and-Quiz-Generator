# main.py

import os
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer

from rag import RAGRetriever
from summarizer import Summarizer
from key_takeaway_generator import KeyTakeawayGenerator
from faq_generator import FAQGenerator
from practice_question_generator import parse_practice_questions
from weaviate_handler import WeaviateHandler

from langchain_groq import ChatGroq

# ── 1) ENV & MODEL SETUP ─────────────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "llama3-8b-8192")

# 1a) Local embedding model (cached)
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> list[list[float]]:
    # returns list of embedding vectors
    return embedder.encode(texts, convert_to_numpy=True).tolist()

# 1b) Groq LLM (for summarization, FAQs, practice questions)
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL,
    temperature=0.7,
    max_tokens=1024,
)

# ── 2) PDF → CHUNKS → EMBEDDINGS → WEAVIATE ────────────────────────────────────────
# Adjust max_pages as desired
from pdf_extraction import extract_text_as_documents
from chunking import chunk_texts

docs   = extract_text_as_documents("test1.pdf", max_pages=3)
chunks = chunk_texts(docs)
valid_chunks    = [c for c in chunks if c.page_content.strip()]
text_chunks     = [c.page_content for c in valid_chunks]
metadata_chunks = [c.metadata     for c in valid_chunks]

print(f"📄 Embedding {len(text_chunks)} chunks…")
for i, txt in enumerate(text_chunks):
    print(f"  [{i}] {txt[:60].replace(chr(10),' ')}…")

embeddings = embed_texts(text_chunks)
if not embeddings:
    print("❌ Embedding failed.")
    exit()

weaviate_handler = WeaviateHandler(collection_name="LectureSlides")
weaviate_handler.insert_chunks(text_chunks, embeddings, metadata_chunks)

# ── 3) RAG RETRIEVAL ───────────────────────────────────────────────────────────────
retriever = RAGRetriever(collection_name="LectureSlides", embedding_model=embedder)
query     = "Give a summary of the lecture content."
retrieved = retriever.retrieve(query, k=15)

# ── 4) SUMMARIZATION ───────────────────────────────────────────────────────────────
summarizer = Summarizer(llm=llm)
summary     = summarizer.summarize(retrieved, question=query)
print("\n📝 Summary:\n", summary.strip())

# ── 5) KEY TAKEAWAYS ───────────────────────────────────────────────────────────────
ktg       = KeyTakeawayGenerator(llm=llm)
takeaways = ktg.generate_takeaways(retrieved)
print("\n📌 Key Takeaways:\n", takeaways.strip())

# ── 6) FAQS ────────────────────────────────────────────────────────────────────────
faqg = FAQGenerator(llm=llm)
faqs = faqg.generate_faqs_from_chunks(retrieved, max_faqs=14)
print("\n❓ FAQs:")
for faq in faqs:
    print(f"Q: {faq['question']}\nA: {faq['answer']}\n")


# ── 7) PRACTICE QUESTIONS ─────────────────────────────────────────────────────────

print("\n🧠 Practice Questions:")
for i, chunk in enumerate(valid_chunks):
    prompt = f"""
Generate 2 multiple-choice questions and 1 open-ended question from the following content. 

Each MCQ should have 4 options labeled A) to D), followed by the correct answer in the format: 'Correct answer: <your answer>'.

Each open-ended question should be preceded by '**Open-ended question:**'.

Content:
\"\"\"
{chunk.page_content}
\"\"\"
"""
    try:
        raw_output = llm.invoke(prompt)
        print(f"\n💬 Raw LLM Output for Chunk {i+1}:\n{raw_output.content}\n")
        parsed_questions = parse_practice_questions(raw_output.content)
    except Exception as e:
        print(f"❌ Failed to generate questions for chunk {i+1}: {e}")
        continue

    print(f"[Chunk {i+1}]")
    
    for q in parsed_questions:
        if "type" not in q:
            print("⚠️ Skipping malformed question:", q)
            continue
    
        if q["type"] == "mcq":
            print(f"Q: {q['question']}")
            for j, option in enumerate(q["options"]):
                print(f"  {chr(65 + j)}) {option}")
            print(f"✔ Answer: {q['answer']}\n")
    
        elif q["type"] == "open":
            print(f"Q (Open-ended): {q['question'].strip()}\n")
    



# ── 8) CLEAN UP ───────────────────────────────────────────────────────────────────
retriever.close()
weaviate_handler.close()
