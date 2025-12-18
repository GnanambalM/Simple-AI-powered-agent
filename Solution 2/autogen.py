from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from groq import Groq
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()

HEADERS = {"User-Agent": "Mozilla/5.0 (AutoGen Research Agent)"}
KEYWORDS = ["about","company","product","service","solution","platform","privacy","policy","terms"]

def get_relevant_links(base_url, max_pages=5):
    try:
        soup = BeautifulSoup(requests.get(base_url, headers=HEADERS, timeout=10).text,"html.parser")
    except Exception:
        return []
    links=set()
    for a in soup.find_all("a", href=True):
        if any(k in a["href"].lower() for k in KEYWORDS):
            full=urljoin(base_url,a["href"])
            if urlparse(full).netloc==urlparse(base_url).netloc:
                links.add(full)
    return list(links)[:max_pages]

def extract_text(url, limit=3000):
    try:
        soup=BeautifulSoup(requests.get(url,headers=HEADERS,timeout=10).text,"html.parser")
        for t in soup(["nav","footer","header"]): t.decompose()
        return soup.get_text(" ",strip=True)[:limit]
    except Exception:
        return ""
company_url="https://nimblebiz.ai/"

content=extract_text(company_url)
for link in get_relevant_links(company_url):
    content+="\n"+extract_text(link)
content=content[:8000]

llm_config={
    "model":"llama-3.1-8b-instant",
    "temperature":0.3
}

planner=AssistantAgent(
    name="Planner",
    system_message="Decide what company information should be extracted.",
    llm_config=llm_config
)

extractor=AssistantAgent(
    name="Extractor",
    system_message="Extract factual public company information only.",
    llm_config=llm_config
)

synthesizer=AssistantAgent(
    name="Synthesizer",
    system_message="""
Return ONLY valid JSON with fields:
company_overview,
products_services,
brand_positioning,
public_policies
""",
    llm_config=llm_config
)

user=UserProxyAgent(
    name="User",
    human_input_mode="NEVER"
)

user.initiate_chat(planner, message=content)
planner.initiate_chat(extractor, message=content)
extractor.initiate_chat(synthesizer, message="Generate final JSON summary")
