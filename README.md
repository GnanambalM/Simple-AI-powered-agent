# Simple-AI-powered-agent

Approach Taken

The solution implements a custom AI-powered research agent that:

Fetches publicly accessible pages from a company’s official website.

Identifies relevant internal links (About, Products, Services, Policies).

Extracts meaningful textual content while removing navigation and layout noise.

Uses a Large Language Model to generate a structured company summary, strictly based on the extracted public content.

The agent is designed to be modular, readable, and aligned with real-world data collection constraints.

Assumptions Made

The company’s official website contains sufficient publicly accessible static content.

Relevant information is available on commonly named pages (e.g., About, Products, Services).

The LLM is used only for summarization and not for external knowledge inference.

API keys are provided securely via environment variables.

Known Limitations

JavaScript-heavy websites may expose limited content through static scraping.

Very large websites may require stricter content limits due to LLM token constraints.

The summary quality depends on the clarity and completeness of the website’s public content.
