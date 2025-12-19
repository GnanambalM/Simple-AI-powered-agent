# Simple-AI-powered-agent

# Solution 1: Custom AI-Powered Company Research Agent

## Approach Taken

This solution implements a custom AI-powered agent that collects publicly available
information from a company’s official website and generates a structured summary.

The agent:
- Fetches the company homepage
- Identifies relevant internal pages (About, Products, Services, Policies)
- Extracts meaningful text while removing navigation and layout noise
- Uses a Large Language Model to summarize the extracted content in a structured format

Only publicly available website content is used for summarization.

---

## Assumptions Made

- The company website contains sufficient publicly accessible information
- Relevant information is available on commonly named pages (e.g., About, Products, Services)
- The LLM is used strictly for summarization, not for external knowledge inference
- API keys are provided securely via environment variables

---

## Known Limitations

- JavaScript-heavy websites may expose limited content through static scraping
- Very large websites may require stricter token limits due to model constraints
- Summary quality depends on the clarity and completeness of website content

---

#  Solution-2-AutoGen

## Approach Taken

This solution explores using an AutoGen-based multi-agent framework to solve the same
problem through agent collaboration.

The design includes:
- A planning agent to decide what information to extract
- A summarization agent to generate the structured company overview
- Clear task separation between agents

This approach demonstrates how the problem can be modeled using agent-based orchestration.

---

## Assumptions Made

- AutoGen agents can coordinate tasks through message passing
- Website content is provided or extracted via external tools
- The solution focuses on agent design rather than full execution

---

## Known Limitations

- AutoGen requires stable multi-agent runtime orchestration
- Execution output is not included due to environment constraints
- The implementation demonstrates design intent rather than a production-ready pipeline

---

