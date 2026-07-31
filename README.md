# 🚌 Smart Transit & Commuter Agent (Bangladesh)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://transit-agent.streamlit.app/) 
[![Python 3.13](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Google AI Studio](https://img.shields.io/badge/Powered%20by-Gemma%204-orange)](https://ai.google.dev/)

An autonomous AI agent designed to help university students in Bangladesh dynamically plan safe and efficient commuter routes around severe traffic, monsoon waterlogging, and budget constraints. 

Built for the **Autonomous Agent Track**, this project demonstrates the native **Function Calling** capabilities of **Gemma 4** to interact with localized external APIs.

---

## 🚀 Live Demo
**[Click here to test the live agent on Streamlit Community Cloud](https://transit-agent.streamlit.app/)**

*(Note: If you run out of budget or encounter an error, you can easily run this locally by following the steps below).*

---

## 🧠 Hackathon Scope: Autonomous Agent Track
This project fulfills the track requirements by leveraging the **Gemma 4 31B Instruct** model via the Google GenAI SDK. Instead of hard-coded if/else statements, the agent autonomously reasons through user prompts and executes real-time function calls to local tools:

1. **`check_waterlogging(area)`**: A localized mock API that alerts the agent to flooded streets in areas like Bahaddarhat or Agrabad.
2. **`estimate_pathao(pickup, dropoff)`**: A mock ride-sharing API simulating dynamic surge pricing for Bikes and CNGs based on demand.

The agent receives the JSON outputs from these tools and formulates a final, contextual travel plan for the commuter.

---

## 🛠️ Tech Stack & Architecture

* **UI & Hosting:** [Streamlit](https://streamlit.io/) & Streamlit Community Cloud (100% Free, zero-cost deployment).
* **AI Model:** `gemma-4-31b-it` (via [Google AI Studio Free Tier](https://aistudio.google.com/)).
* **Agent Framework:** None. Uses the native **Google GenAI Python SDK** for faster, token-efficient function calling without the overhead of LangChain.

---

## 💻 How to Run Locally

To test the agent's thought process and function-calling debugger on your own machine, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/sheikh-mohammad-rakib/transit-agent.git
cd transit-agent
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API Key
You can provide your Gemini API key in one of three ways:
* Add it to a `.env` file: `GEMINI_API_KEY="your_api_key_here"`
* Add it to `.streamlit/secrets.toml`: `GEMINI_API_KEY="your_api_key_here"`
* Enter it directly in the Streamlit UI sidebar when you run the app.

### 5. Run the Application
```bash
streamlit run app.py
```