# 📚 Automated Lecture Summarizer and Quiz Generator


## 🚀 Project Overview

This project is a powerful educational tool that helps students quickly absorb and revise lecture materials (text transcripts or PDFs like slides) using Natural Language Processing (NLP). It transforms dense content into:

- 🔹 **Concise Summaries**  
- 🔹 **Key Takeaways**  
- 🔹 **FAQ-style Answers**  
- 🔹 **Practice Questions with Answers**

Built using a **Retrieve-and-Generate (RAG)** approach with modern transformer-based LLMs, the app simplifies learning, aids exam prep, and enables fast revision.

---

## 🧠 Core Features

### ✅ Input Formats
- Accepts **PDF slides** or **plain text transcripts** as input

### ✅ Output Tabs
- **Summary Tab**: Concise paragraph-style summary
- **Key Takeaways Tab**: Bullet-point takeaways
- **FAQs Tab**: FAQ-style Q&A from content
- **Practice Q&A Tab**: Factual, conceptual, MCQs, and open-ended Q&As

### ✅ Text Extraction
- Uses `PyMuPDF` for extracting text from PDFs
- Supports **lazy loading** (one page at a time)
- Chunking handled **during extraction** using:
  - `RecursiveCharacterTextSplitter`
  - Adaptive chunk size (256–512 tokens)
  - 20% overlap for context preservation

### ✅ NLP Pipeline
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector DB**: `Weaviate` with metadata filtering
- **LLMs Used**: `LLaMA3` and `Mistral`
- **FAQ + Question Generator**:
  - Structured prompts per type (factual, conceptual, MCQ, open-ended)
  - Two-step process: Generate candidates → Re-rank → Finalize
  - Re-ranking via Cohere Rerank API

### ✅ UI (Streamlit)
- Tabs for each output type
- File uploader (PDF or TXT)
- Secure API key input (not stored)
- Feedback system with thumbs up/down + optional comment box

### ✅ Backend Processing
- Parallel processing with `concurrent.futures`
- OCR fallback for non-textual elements (tables/images)
- Optional web search if OCR fails
- Metadata stored per chunk:
  - Page number
  - Section header
  - Chunk index
  - Filename/title
  - Auto-generated keywords/tags

---

## 🔧 How to Run Locally

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/lecture-summarizer.git
cd lecture-summarizer
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Start the Streamlit App
```bash
streamlit run main.py
```

> **Note**: You’ll be prompted to enter your Hugging Face and Cohere API keys in the Streamlit UI.

---

## ☁️ Deployed App
You can try out the deployed version here: [https://lecture-summarizer.streamlit.app](https://lecture-summarizer.streamlit.app) *(Replace with actual link)*

---

## 📊 Example Use Case

A student uploads a PDF of ML lecture slides. The tool outputs:

- **Summary**: One-paragraph overview of all slides
- **Key Takeaways**: Bullet list of core ideas
- **FAQs**: “What is supervised learning?” → "Supervised learning is..."
- **Practice Q&A**: “What are the advantages of decision trees?” + answer

---

## 🔮 Future Enhancements

- ❓ Answer user’s custom questions (QA over indexed documents)
- 📝 Graded quizzes with timer simulation
- 📊 Support for tables and images (enhanced OCR & multimodal models)
- 🎯 Adaptive feedback-driven improvements to RAG pipeline

---

## 🧪 Evaluation Criteria

| Criteria         | Description |
|------------------|-------------|
| Functionality     | How well it performs the summarization, FAQ, and question generation tasks |
| User Experience   | Clarity and ease of use of the UI |
| Code Quality      | Modularity, documentation, and maintainability |
| Innovation        | Unique features, smart enhancements, and scalable design |

---

## 📁 Project Structure

```
lecture-summarizer/
├── main.py                        # Streamlit frontend + pipeline integration
├── summarizer.py                 # Handles summarization logic
├── key_takeaway_generator.py     # Bullet-point takeaway generation
├── faq_generator.py              # Chunk-based FAQ generation
├── practice_question_generator.py# Multiple-type question generation
├── pdf_loader.py                 # PyMuPDF-based loader with chunking & metadata
├── retriever.py                  # Vector DB + embedding + retrieval setup
├── reranker.py                   # Cohere/Hugging Face re-ranking logic
├── utils.py                      # Helper utilities for prompts, API wrappers, etc.
├── requirements.txt
└── README.md
```

---

## 🔐 API Key Handling

- Users enter HuggingFace & Cohere API keys securely in the frontend
- Keys are stored temporarily in Streamlit's session state
- No keys are stored in backend or logs

---

## 💬 Feedback System

Each output tab includes:
- 👍 / 👎 buttons
- Optional text comment box
- Stores feedback for future improvements and tuning

---

## 🛠 Tech Stack

- Python 3.10+
- PyMuPDF (text extraction)
- LangChain (RAG pipeline)
- Weaviate (vector database)
- Sentence Transformers (MiniLM-L6-v2)
- Hugging Face Inference API (LLMs + rerankers)
- Cohere Rerank API
- Streamlit (UI)

---

## ✨ Credits

.

---

## 📽️ Deliverables

- ✅ GitHub Repo (with instructions)
- ✅ Deployed Web App
- ✅ Video Demo
- ✅ README (this file)

---

## 🧠 Final Thought

This project lays a solid foundation for future educational tech tools by making dense lecture content accessible, interactive, and actionable.

Happy Learning! 🎓

