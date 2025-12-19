# Project Documentation  
Simple AI-Powered Company Research Agent

---

## 1. Project Overview

This project implements an AI-powered agent that collects publicly available
information about a given company from its official website and generates a
structured company summary.

The objective is to demonstrate:
- Web data collection and preprocessing
- Responsible use of LLMs for summarization
- Clean software design and modularity
- Secure handling of API credentials

The repository contains two independent solutions:
1. A custom-built AI research agent (primary solution)
2. An exploratory AutoGen-based multi-agent design

---

### Technologies Used

- Python 3
- Requests
- BeautifulSoup
- Groq LLM API
- Autogen
- python-dotenv (for environment variable handling)

---

### Execution Flow

1. Normalize the provided company URL
2. Fetch the homepage content
3. Discover relevant internal links (About, Products, Services, Policies)
4. Extract and clean textual content
5. Combine extracted text
6. Generate a structured summary using an LLM

---

### Environment Setup

#### Install Dependencies
```bash
pip install -r requirements.txt

---

#### API Key Configuration
Create a .env file locally:
```bash
GROQ_API_KEY=your_groq_api_key

---

#### Running the Agent
```bash
python agent.py

Update the target company URL inside agent.py as needed.
