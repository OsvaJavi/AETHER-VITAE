# Work Plan: Space Biology Knowledge Engine (Aethr Vitae)

This work plan is divided into **six main phases**, assuming a weekend timeframe (approximately 48–72 hours).

## Phase 0: Preparation and Environment Setup (Duration: 2 hours)

**Objective:** Establish a solid and organized working environment to prevent technical issues later. A good start is half the battle.

**Key Tools:** Git, GitHub, Python 3.9+, pip, Visual Studio Code (or your preferred editor)

### Concrete Actions

**1. Create the Repository:**  
Start a new GitHub repository for the project and clone it locally.

**2. Folder Structure:**  
Create a clean and logical folder structure:

/nasa-knowledge-engine
|-- /data               # To store raw and processed data
|-- /notebooks          # For initial exploration and testing (optional)
|-- app.py              # Main Streamlit app file
|-- requirements.txt    # Python dependencies
|-- .env                # Securely store your Groq API key
|-- .gitignore          # Ignore unnecessary files
3. Virtual Environment:
Create and activate a Python virtual environment to isolate dependencies.

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
4. Install Dependencies: Create a requirements.txt file and add initial libraries:

streamlit
groq
sentence-transformers
numpy
pandas
python-dotenv
Then install them:

pip install -r requirements.txt
5. Configure API Key: Create a .env file and add your Groq API key.

GROQ_API_KEY="your-api-key-here"
6. Initial Verification: Create a basic app.py to ensure Streamlit runs properly.

import streamlit as st
st.title("🚀 Space Biology Knowledge Engine")
st.write("Welcome to the NASA Challenge!")
Run:

streamlit run app.py
Expected Outcome: A configured project, clean environment, and a working Streamlit app.

Phase 1: Data Collection and Processing (Duration: 3–4 hours)
Objective: Retrieve the text of the 608 scientific papers and store it in a structured, easy-to-use format.

Key Tools: pandas, requests, BeautifulSoup4 (for web scraping)

Concrete Actions
Locate the Source: Find the online repository containing the list of 608 publications mentioned in the challenge resources.

Create a Data Extraction Script: Write a Python script (you may use a Jupyter notebook in /notebooks) that:

Accesses the data source
Extracts the title, authors, year, and especially the abstract of each publication
Plan B: If full-text access is available via API or download, use it; otherwise, abstracts are sufficient and realistic for a hackathon.

Clean the Text: Perform basic cleaning (remove extra newlines, unwanted symbols, etc.).

Save in Structured Format: Store the cleaned information as a single CSV or JSON file in /data.

Suggested columns: id, title, authors, year, abstract_text, source_url

Expected Outcome: A clean file (publications.csv or .json) ready for AI processing.

Phase 2: Semantic Search Engine – Embeddings (Duration: 2–3 hours)
Objective: Convert each publication’s text into numerical vectors (embeddings) to enable semantic search (meaning-based rather than keyword-based).

Key Tools: sentence-transformers, numpy

Concrete Actions
Create an Indexing Script: Write create_embeddings.py — a script that runs once to prepare the dataset.

Load the Data: Read the CSV created in Phase 1.

Load a Pre-trained Model: Use a lightweight, high-quality embedding model:

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
Generate Embeddings:
corpus_embeddings = model.encode(df['abstract_text'].tolist(), convert_to_tensor=True)
Save Embeddings:
import numpy as np
np.save('data/corpus_embeddings.npy', corpus_embeddings.cpu().numpy())
Expected Outcome: A file corpus_embeddings.npy containing the vector representation of all publications.

Phase 3: Backend – AI Logic with Groq (Duration: 4–5 hours)
Objective: Build Python functions that interact with the Groq API to summarize text and extract key entities in real time.

Key Tools: groq, os, python-dotenv

Concrete Actions
Semantic Search Function: In app.py, create a function search(query, top_k=5) that:

Takes the user query
Encodes it into an embedding using the same model
Computes cosine similarity between the query and corpus embeddings
Returns top_k results
Groq Client Configuration: Set up the Groq client to read the API key from .env.

Prompt Engineering – Summarization Function:

You are a NASA bioscience expert. 
Summarize the following text in 3 key points focusing on:
- The experiment conducted
- Main results
- Implications for human space exploration
The summary should be clear and concise.
Prompt Engineering – Entity Extraction Function:

Analyze the following scientific text and extract the following entities in JSON format:
{
  "organism": "...",
  "condition": "...",
  "key_finding": "..."
}
If an entity is not found, use "N/A".
Expected Outcome: Robust, reusable Python functions for searching, summarizing, and extracting entities, ready for frontend integration.

Phase 4: Frontend – Interactive Dashboard with Streamlit (Duration: 5–6 hours)
Objective: Build an interactive user interface to display information clearly and dynamically.

Key Tool: Streamlit

Concrete Actions
Interface Design: Sketch the app layout — typically a sidebar for filters and a main area for results.

Main Search Bar: Use st.text_input for the query field.

App Logic:

Load data (.csv) and embeddings (.npy) once at startup using @st.cache_data
On user search, call search()
Display results dynamically using expanders or containers
Display Results:

Title, authors, and year
Summary via get_summary()
Entities via extract_entities() (display with st.json or st.metric)
Use st.spinner for loading animations
Bonus – Visualizations:

In the sidebar, show bar charts of common organisms or research topics
Expected Outcome: A fully functional, interactive Streamlit web app for exploring NASA publications.

Phase 5: Integration, Testing, and Refinement (Duration: 3–4 hours)
Objective: Integrate all components, test the workflow, and enhance user experience.

Key Tool: Your critical thinking.

Concrete Actions
Perform end-to-end testing with various query types (specific, general, scientific jargon).
Verify relevance of search results and accuracy of summaries.
Tune prompts if outputs are weak — add context, improve formatting, or clarify instructions.
Implement error handling (API failure, empty results). Use st.warning or st.error.
Improve UI/UX with better titles, user instructions, and source credits.
Expected Outcome: A stable, polished, and user-friendly application.

Phase 6: Deployment (Duration: 1–2 hours)
Objective: Put the app online for judges and the public.

Key Tools: Streamlit Community Cloud, GitHub

Concrete Actions
Clean the Repository:

Update requirements.txt
Ensure .env and large datasets are excluded via .gitignore
Deploy on Streamlit Cloud:

Push your project to GitHub
Visit share.streamlit.io
Connect your GitHub account
Select the repository, main branch, and app.py
Add the Groq API key as a secret, not hardcoded
Documentation: Write a concise README.md describing what the project does, how it was built, and how to use it.

Expected Outcome: A public, accessible URL of your live Streamlit app — ready for presentation. 🎉
