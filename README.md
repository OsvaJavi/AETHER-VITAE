
```markdown
# 🌌 AETHER VITAE – NASA Space Biology Challenge 2025

> **“Exploring the intersection of biotechnology and the space frontier.”**

## 🚀 Project Overview

**AETHER VITAE** is an AI-powered knowledge engine designed to explore and analyze NASA’s **608 scientific publications on space biology**.  
It integrates a **semantic search engine**, **automated summarization**, and **entity extraction** powered by **Groq + Llama 3** and **Sentence Transformers**, enabling scientists and students to discover insights faster.

This project includes both a **visual portal** and a **Streamlit AI assistant**, forming an interactive ecosystem for scientific discovery.

## 🧠 Core Features

- 🔍 **Semantic Search:** Find publications by meaning, not just by keywords.  
- 🧾 **AI Summaries:** Generate concise, three-point summaries using LLMs.  
- 🧬 **Entity Extraction:** Identify organisms, conditions, and findings automatically.  
- 📊 **Interactive Visualizations:** Dashboard with statistics and graphs.  
- ⚡ **Real-Time Response:** Fast inference powered by precomputed embeddings.  
- 🌕 **Dynamic Portal:** Users can enter through celestial nodes (Moon, Mars, ISS, Life) that redirect to AI-driven searches.

## 🛠️ Technologies Used

| Layer | Technologies |
|-------|---------------|
| **Frontend (Portal)** | HTML, TailwindCSS, JavaScript |
| **AI Backend** | Python 3.9+, Groq API (Llama 3) |
| **Framework** | Streamlit |
| **Embeddings** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Data Handling** | Pandas, NumPy |
| **Automation** | Custom Python script for NASA paper download |

---

## 📁 Project Structure

```

AETHER-VITAE/
├── 📂 data/
│   ├── publications.csv           # NASA’s 608 space biology papers metadata
│   ├── corpus_embeddings.npy      # Precomputed semantic embeddings
│   └── nasa_pdfs/                 # Folder for downloaded PDF files
│
├── 📂 notebooks/
│   └── exploration.ipynb          # Exploratory data analysis (optional)
│
├── 📂 web/
│   ├── index.html                 # Landing page ("Aether Vitae Portal")
│   ├── curious.html               # Educational/Space Explorer page
│   ├── about.html                 # About / Contact section
│   ├── public/
│   │   ├── logo.png               # Project logo
│   │   ├── deep-space.png         # Background image
│   │   ├── iss.png, mars.png, moon.png, earth.png  # Celestial icons
│   │   └── favicon.ico            # Browser icon
│   └── styles.css (optional)      # Extracted custom CSS
│
├── 📂 bot/
│   ├── app.py                     # Main Streamlit AI app
│   ├── create_embeddings.py       # Script to generate text embeddings
│   ├── download_papers.py         # Automated NASA paper downloader
│   └── utils/                     # Helper functions (search, summarization, etc.)
│
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (API keys)
├── .gitignore                     # Ignored files and folders
└── README.md                      # This document

````

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/OsvaJavi/AETHER-VITAE.git
cd AETHER-VITAE
````

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your-api-key-here
```

💡 Get a free API key at [https://console.groq.com](https://console.groq.com)

## 🧩 Data Preparation

### Option A – Use Existing Data

Place your `publications.csv` file inside the `/data` folder with these columns:

| Column        | Description           |
| ------------- | --------------------- |
| id            | Unique identifier     |
| title         | Publication title     |
| authors       | Authors               |
| year          | Year of publication   |
| abstract_text | Abstract or summary   |
| source_url    | Source URL (optional) |

### Option B – Download from NASA Automatically

Run the provided script to download all papers and generate the CSV:

```bash
python bot/download_papers.py
```

## 🧮 Generate Embeddings

Convert abstracts into semantic vectors using Sentence Transformers:

```bash
python bot/create_embeddings.py
```

This creates `data/corpus_embeddings.npy` used for fast semantic search.

## 🛰️ Run the Streamlit App

Launch the intelligent search assistant:

```bash
streamlit run bot/app.py
```

Your app will open at **[http://localhost:8501](http://localhost:8501)**

To deploy it publicly, visit **[streamlit.io/cloud](https://streamlit.io/cloud)** and connect your GitHub repository.

## 💻 How to Use

1. **Visit the Portal:**
   Open `web/index.html` in your browser.
   Click on any celestial node (🌕 Moon, 🔴 Mars, 🛰 ISS, 🌍 Life).

2. **Automatic Query:**
   Clicking a node redirects you to
   [https://aether-vitae-bot.streamlit.app](https://aether-vitae-bot.streamlit.app)
   preloaded with a query like “moon” or “mars”.

3. **Explore Results:**

   * View NASA publications by meaning (semantic similarity).
   * Read auto-generated summaries and extracted key entities.
   * Filter by organism, condition, or year.

## 🧠 Example Queries

* “How does microgravity affect human cells?”
* “Radiation impact on DNA during spaceflight”
* “Experiments with *C. elegans* on the ISS”
* “Plant growth under lunar gravity simulations”

## 🎯 Challenges Solved

✅ **Efficient Search:** Precomputed embeddings enable sub-second retrieval.
✅ **Contextual Summarization:** LLM-powered, domain-specific synthesis.
✅ **Entity Extraction:** Structured insights via JSON output.
✅ **Educational Gateway:** Engaging visual interface bridging science and AI.

## 🧭 Future Improvements

* 🔍 Advanced filters by organism and condition type
* 🕸️ Knowledge graph of interconnected studies
* 🗂️ Export search results as PDF or CSV
* 💬 Interactive chatbot using the full corpus
* 🌐 Multi-language support (EN/ES)

## 👨‍🚀 Authors

Developed by **Team Aether Vitae**
for the **NASA Space Biology Challenge – Guadalajara 2025**

Víctor Hugo López Martín

🎯 Project Manager & Team Coordinator
Project planning, coordination, and time management. Oversees documentation and NASA Challenge submissions.
📧 victor.lmartin@alumnos.udg.mx

Martín Ángel Carrizales Piña

🧠 Data Scientist
Develops and trains the machine learning models for biosignature detection and data interpretation.
📧 martin.carrizalez0823@alumnos.udg.mx

Miguel Isay Morales Cortés

💡 Marketing & Branding Lead
Designs and manages the project’s branding, social media presence, and official website.
📧 isay.morales@alumnos.udg.mx

Óscar Vicente Coronado Orozco

📊 Data Engineer
Builds the code infrastructure to extract and process scientific articles forming the project’s core database.
📧 oscar.coronado6444@alumnos.udg.mx

Oswaldo Javier Rojas del Toro

⚙️ Operations & AI Developer
Supports deployment, model integration, and repository maintenance on GitHub.
📧 oswaldo.rojas6815@alumnos.udg.mx

Miguel Omar Flores García

🔍 Data Acquisition Specialist
Collects and curates scientific data sources manually to feed the training datasets.
📧 miguel.flores6629@alumnos.udg.mx


## 📄 License

This project is open-source under the **MIT License**.


## 🙏 Acknowledgments

* **NASA** – For providing open access to the Space Biology dataset
* **Groq** – For enabling fast LLM inference
* **Streamlit Community** – For intuitive and powerful web tools
* **University of Guadalajara (CUGDL)** – For supporting the initiative


### 🌠 Live Demo

🔗 **Portal:** [https://aether-vitae.netlify.app/](#) *(optional)*
🔗 **AI Assistant:** [https://aether-vitae-bot.streamlit.app/](https://aether-vitae-bot.streamlit.app/)

```
