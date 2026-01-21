# 🚀 AI Project Requirement Analyzer

An AI-powered system that converts vague, non-technical project ideas into **clear, structured, and actionable AI project requirements** using **Retrieval-Augmented Generation (RAG)**.

---

## 📌 Problem Statement

AI consulting companies often face a recurring challenge:

> Clients describe their ideas vaguely (e.g., *“I need AI for my business”* or *“Build me a chatbot”*), leading to multiple back-and-forth discussions before clear requirements are formed.

This consumes senior consultants’ time and slows down project initiation.

### ✅ Solution

This project automates **initial AI requirement analysis** by:

* Understanding vague user ideas
* Retrieving similar past AI projects
* Generating grounded, consultant-style recommendations

---

## 🎯 Key Features

* 🧠 **RAG-based Requirement Analysis**
* 🔍 **Semantic Search over Past AI Projects**
* 📊 **Similarity Scores for Transparency**
* ⚡ **FastAPI Backend (Async & Scalable)**
* 💾 **Local Vector Store using ChromaDB**
* 🤖 **LLM-powered Recommendations via Groq**
* 🌐 **Clean HTML/CSS/JS Frontend**
* 📁 **Production-ready, modular architecture**

---

## 🏗️ System Architecture

```
User Input (Frontend)
        |
        v
FastAPI Backend
        |
        +--> Embedding Service (ChromaDB)
        |
        +--> Vector Search (Top-K Similar Projects)
        |
        +--> Context Builder
        |
        +--> Groq LLM (Llama 3.3 70B)
        |
        v
Structured AI Project Recommendation
```

---

## 🧩 Technology Stack

### 🔹 Backend

* **Python**
* **FastAPI**
* **Groq API** (Llama 3.3 70B Versatile)
* **ChromaDB** (Vector Database + Embeddings)

### 🔹 Frontend

* HTML
* CSS
* Vanilla JavaScript

### 🔹 AI & ML

* Retrieval-Augmented Generation (RAG)
* Sentence-transformer-based embeddings (via ChromaDB)
* Cosine similarity search

---

## 📚 Dataset

* **35 AI Project Case Studies**
* Domains include:

  * Retail
  * Healthcare
  * Finance
  * Media
  * Customer Support
  * Recommendation Systems
* Each project contains:

  * Problem Description
  * AI Approach
  * Tech Stack
  * Outcome

---

## 🔄 How RAG Works (High-Level)

1. **Ingestion**

   * Project cases are converted into text chunks
   * Embedded into 384-dimensional vectors
   * Stored in ChromaDB

2. **Query Processing**

   * User query → embedding
   * Vector similarity search (Top 3 matches)
   * Retrieved projects form contextual grounding

3. **LLM Generation**

   * Groq LLM generates recommendations
   * Uses retrieved projects as factual grounding
   * Avoids hallucination

---

## ▶️ Application Flow

1. User enters a vague AI idea
2. Backend retrieves similar historical projects
3. LLM generates:

   * AI approach
   * Suggested tech stack
   * Implementation direction
4. Frontend displays:

   * AI-generated response
   * Similar projects with similarity scores

---

## 🖥️ Screens (What You’ll See)

* ✔️ Input box for project ideas
* ✔️ AI-generated requirement analysis
* ✔️ Sidebar with similar projects
* ✔️ Real-time backend logs

---

## 🧪 Example Queries

* “I need a customer support chatbot”
* “Build a recommendation system for e-commerce”
* “Analyze customer feedback at scale”
* “Healthcare chatbot with compliance”

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-project-requirement-analyzer.git
cd ai-project-requirement-analyzer
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Environment Variables

Create `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### 5️⃣ Ingest Data

```bash
python ingest.py
```

### 6️⃣ Run Backend

```bash
uvicorn main:app --reload
```

### 7️⃣ Open Frontend

Open `index.html` in browser

---

## 🧠 Why RAG Instead of Fine-Tuning?

| RAG             | Fine-Tuning         |
| --------------- | ------------------- |
| Dynamic updates | Requires retraining |
| Lower cost      | Expensive           |
| Transparent     | Black-box           |
| Scales easily   | Slow iteration      |

---

## 🚧 Challenges Faced

* SSL certificate issues in restricted networks
* Model deprecation on Groq
* Vector DB state management
* Context window size optimization

Each challenge improved real-world engineering skills.

---

## 🔮 Future Improvements

* Conversation memory
* PDF export of requirements
* User authentication
* Multi-language support (Indian languages)
* External data source integration

---

## 📂 Project Structure

```
ai-requirement-analyzer/
│
├── backend/
│   ├── __pycache__/
│   ├── data/
│   │   └── chroma_db/
│   │       ├── chroma.sqlite3
│   │       └── bcbaf7b2-7b1b-47ce-8f8a-dc56d165aa3/
│   │
│   ├── routes/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── chat.py
│   │
│   ├── services/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── rag_pipeline.py
│   │   └── vector_store.py
│   │
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   └── prompts.py
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── models.py
│
├── data/
│   └── sample_ai_projects.json
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── scripts/
│   └── ingest_data.py
│
├── venv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt

```

---

## 📌 Internship Context

* **Company:** Inarva Solutions
* **Assessment Type:** AI Engineering Internship
* **Focus:** RAG, Vector Search, LLM Integration, System Design

---

## 🧾 License

This project is for **educational and evaluation purposes only**.

---

## 🙌 Acknowledgements

* Groq
* ChromaDB
* FastAPI
* Open-source AI community

---

## 📞 Contact

If you have questions or feedback, feel free to reach out.

Explanation video link:https://drive.google.com/file/d/1TJ47n3gBqEd9ka0lqVDiojiNbBLurwDU/view?usp=sharing
