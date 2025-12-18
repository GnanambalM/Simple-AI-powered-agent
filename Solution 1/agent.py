from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from groq import Groq

load_dotenv()

HEADERS = {"User-Agent": "Mozilla/5.0 (Public Research Agent)"}
KEYWORDS = [
    "about", "company", "who-we-are",
    "product", "products", "service", "services",
    "solution", "platform",
    "privacy", "policy", "terms"
]
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def normalize_url(url):
    if url.startswith("https://www."):
        return url.replace("https://www.", "https://")
    if url.startswith("http://www."):
        return url.replace("http://www.", "http://")
    return url

def get_relevant_links(base_url, max_pages=5):
    try:
        response = requests.get(base_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception:
        return []
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if any(k in href for k in KEYWORDS):
            full_url = urljoin(base_url, a["href"])
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                links.add(full_url)
    return list(links)[:max_pages]

def extract_clean_text(url, max_length=8000):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for sel in ["header", "footer", "nav"]:
            for tag in soup.find_all(sel):
                tag.decompose()
        texts = []
        if soup.title and soup.title.string:
            texts.append(soup.title.string)
        for meta in soup.find_all("meta"):
            if meta.get("name") == "description" and meta.get("content"):
                texts.append(meta.get("content"))
            if meta.get("property") in ["og:title", "og:description"] and meta.get("content"):
                texts.append(meta.get("content"))
        for h in soup.find_all(["h1", "h2", "h3"]):
            txt = h.get_text(strip=True)
            if len(txt) > 5:
                texts.append(txt)
        for tag in soup.find_all(["a", "button"]):
            txt = tag.get_text(strip=True)
            if len(txt) > 15:
                texts.append(txt)
        body = soup.body.get_text(separator=" ", strip=True) if soup.body else ""
        if body:
            texts.append(body)
        final_text = " ".join(texts)
        return final_text[:max_length]
    except Exception:
        return ""

class CompanyResearchAgent:
    def __init__(self, base_url):
        self.base_url = normalize_url(base_url)
    def run(self):
        collected_text = ""
        collected_text += extract_clean_text(self.base_url) + "\n"
        pages = get_relevant_links(self.base_url)
        for page in pages:
            collected_text += extract_clean_text(page) + "\n"
        if len(collected_text.strip()) < 300:
            return "Public website content is minimal or JavaScript-rendered. Summary generated using metadata only."
        return self.summarize(collected_text)
    def summarize(self, content):
        prompt = f"""
You are an AI research assistant.
Using ONLY the publicly available website content below, generate a structured company summary in Markdown with: 
### 1. What the company does (1–2 paragraphs) 
### 2. Products / Services offered - Bullet points 
### 3. Brand positioning or uniqueness - 2–3 bullet points 
### 4. Public policies mentioned - Bullet points (if any) 
Website Content: 
{content}
"""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
if __name__ == "__main__":
    company_url = "https://nimblebiz.ai/"
    agent = CompanyResearchAgent(company_url)
    output = agent.run()
    print(output)
