# 🧠 HyperMind AI

### Supercharge your academics, finance & campus life with Groq-powered intelligence.

HyperMind is a premium, all-in-one AI student assistant designed to streamline your college experience. Built with **Streamlit** and powered by **LLaMA 3.3 70B via Groq**, it delivers lightning-fast, high-quality responses for every student need.

---

## 🚀 Features

*   📅 **Smart Daily Planner** – Enter tasks and get an AI-prioritized schedule.
*   📊 **AI Grade Predictor** – Calculate exactly what you need in finals to hit your goals.
*   💰 **Budget Advisor** – Smart spending plans tailored for students.
*   🤔 **Decision Helper** – Logical pros/cons analysis for your dilemmas.
*   🛡️ **Scam Checker** – Instant analysis of suspicious links and messages.

---

## 🛠️ Tech Stack

*   **Frontend:** Streamlit (Custom Premium CSS)
*   **LLM:** LLaMA 3.3 70B
*   **API:** Groq Cloud
*   **Language:** Python

---

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/darshanmgani-glitch/Hypermind.git
    cd Hypermind
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables:**
    Create a `.env` file in the root directory and add your Groq API Key:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

---

## 🛡️ Security
This project uses a `.gitignore` to ensure that `.env` files and sensitive API keys are **never** committed to version control. Please ensure you keep your `GROQ_API_KEY` private.

---

## 📄 License
This project is licensed under the MIT License.
