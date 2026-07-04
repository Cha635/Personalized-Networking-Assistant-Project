# Personalized Networking Assistant

An AI-powered web application that helps users prepare for professional networking events by generating personalized conversation starters. The system analyzes event descriptions, identifies key discussion topics, generates meaningful conversation starters, and verifies important information using the Wikipedia API.

---

## 📌 Overview

The Personalized Networking Assistant is designed to enhance networking experiences by helping users initiate engaging and relevant conversations during professional events.

The application leverages Natural Language Processing (NLP) and Generative AI techniques to:

- Analyze event descriptions
- Extract important event topics
- Generate personalized conversation starters
- Verify extracted topics using Wikipedia
- Maintain conversation history and user feedback

The project consists of a **FastAPI backend** and a **Streamlit frontend**.

---

## ✨ Features

- Event description analysis
- Personalized interest-based conversation starters
- Event theme extraction using DistilBERT
- Conversation generation using GPT-2
- Wikipedia-based fact verification
- Conversation history logging
- User feedback logging
- FastAPI REST API integration
- Streamlit web interface
- Input validation

---

## 🛠️ Technology Stack

- Python 3.11
- Streamlit
- FastAPI
- Hugging Face Transformers
- DistilBERT (Zero-Shot Classification)
- GPT-2
- Wikipedia API
- Pytest

---

## 📂 Project Structure

```

Personalized-Networking-Assistant-Project/
│
├── 1. Brainstorming & Ideation/
│   ├── Brainstorming & Idea Prioritization.pdf
│   ├── Define Problem Statements.pdf
│   └── Empathy Map.pdf
│
├── 2. Requirement Analysis/
│   ├── Customer Journey Map.pdf
│   ├── Data Flow Diagram.pdf
│   ├── Solution Requirements.pdf
│   └── Technology Stack.pdf
│
├── 3. Project Design Phase/
│   ├── Problem-Solution Fit.pdf
│   ├── Proposed Solution.pdf
│   └── Solution Architecture.pdf
│
├── 4. Project Planning Phase/
│   └── Project Planning.pdf
│
├── 5. Project Development Phase/
│   ├── Code-Layout, Readability and Reusability.pdf
│   ├── Coding & Solution.pdf
│   ├── No. of Functional Features Included.pdf
│   ├── project/
│   │   ├── .streamlit/
│   │   ├── app/
│   │   ├── data/
│   │   ├── frontend/
│   │   ├── tests/
│   │   ├── .env.example
│   │   ├── .gitignore
│   │   ├── README.md
│   │   └── requirements.txt
│   └── Project_Demo_Video.mp4
│
├── 6. Project Testing/
│   └── Performance Testing.pdf
│
├── 7. Project Documentation/
│   ├── Project Executable Files.pdf
│   └── Sample Project Documentation.pdf
│
├── 8. Project Demonstration/
│   ├── Communication.pdf
│   ├── Demonstration of Proposed Features.pdf
│   ├── Project Demo Planning.pdf
│   ├── Scalability & Future Plan.pdf
│   └── Team Involvement in Demonstration.pdf
│
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the project directory

```bash
cd Personalized-Networking-Assistant-Project/5.\ Project\ Development\ Phase/project
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 5. Install the dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

### Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

### Start the Streamlit frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

## 🧪 Testing

Run the test suite using:

```bash
pytest
```

---

## 📑 Project Documentation

The repository is organized into the following project phases:

1. Brainstorming & Ideation
2. Requirement Analysis
3. Project Design Phase
4. Project Planning Phase
5. Project Development Phase
6. Project Testing
7. Project Documentation
8. Project Demonstration

---

## 👥 Team Members

- Maliga Charishma
- Challa Praveenkumar
- Naidu Sashank

---

## 📄 License

This project was developed as part of the **SmartBridge AI-ML & Generative AI Internship Program**.

---

## 🙏 Acknowledgements

- SmartBridge
- APSCHE
- Hugging Face Transformers
- Streamlit
- FastAPI
- Wikipedia API
