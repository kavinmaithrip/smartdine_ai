# 🍽️ SmartDine – AI-Powered Food Recommendation System

SmartDine is an AI-powered food recommendation system that provides **context-aware restaurant and dish suggestions** based on **natural language queries**, **user mood**, **city**, **session memory**, and **optional weather context**.  
The system is designed for students and young professionals to discover food that matches how they feel, not just what they search.

---

## 🚀 Tech Stack

### Frontend
- React.js
- Vite
- Tailwind CSS

### Backend
- FastAPI
- Python
- FAISS (vector search)
- Sentence Transformers
- LLaMA-3 (via Groq API)
- OpenWeather API (optional)

---

## 🧠 AI Approach Used

SmartDine uses a **Full Neural Search Stack**:

1. **Semantic Embeddings** – Sentence Transformers convert food descriptions and user queries into dense vectors  
2. **Vector Search** – FAISS retrieves top-N semantically similar items  
3. **Neural Re-ranking** – Hybrid scoring using semantic similarity + mood + context  
4. **LLM Generation** – LLaMA-3 generates human-like, natural explanations  
5. **Session Memory** – Improves variety and avoids repetitive recommendations  
6. **Optional Weather Awareness** – Softly influences at least one recommendation

---

## 📦 Prerequisites

Ensure the following are installed:

- Python **3.10 or above**
- Node.js **18 or above**
- npm
- Git

---

## 🛠️ Backend Setup

### 1️⃣ Clone the Repository

git clone <repository-url>
cd smartdine

### 2️⃣ Create and Activate Virtual Environment
python -m venv venv


Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate

### 3️⃣ Install Backend Dependencies
pip install -r requirements.txt

### 4️⃣ Environment Variables

Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key


⚠️ Weather API is optional
The application works even without weather data.

### 5️⃣ Run Backend Server
uvicorn backend.api:app --reload


Backend will be available at:

http://localhost:8000


Health check:

http://localhost:8000/health

🌐 Frontend Setup

### 6️⃣ Navigate to Frontend Folder
cd frontend

### 7️⃣ Install Frontend Dependencies
npm install

### 8️⃣ Run Frontend Server
npm run dev


Frontend will be available at:

http://localhost:5173

▶️ How to Use SmartDine

Select a city

Enter a natural language query, for example:

something comforting and cheesy

hot and spicy food

italian but not too heavy

Click Recommend

Click Surprise Me for exploratory suggestions

Repeat queries to observe variation and memory-based behavior

🔗 API Endpoints
Get Cities
GET /cities

Get Recommendations
POST /recommend


Request Body

{
  "query": "something spicy",
  "city": "chennai",
  "surprise": false
}

🧪 Evaluation Notes

Fully neural semantic search pipeline

Context-aware recommendations

LLM explanations with unique wording

No login required; session memory handled internally

Modular, extensible architecture

🧩 Troubleshooting

FAISS installation issue

pip install faiss-cpu


Missing API keys

Ensure .env file exists

Restart backend after updating .env