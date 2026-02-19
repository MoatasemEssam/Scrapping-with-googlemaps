# Scrapping-with-googlemaps
An automated microservices pipeline designed to scrape medical clinic data from Google Maps, process it using a local LLM (Gemma 3 via Ollama), and verify leads for private medical practices in Egypt.

# Features
- Microservices Architecture: Three decoupled services (Scraper, AI Processor, Orchestrator) communicating via REST APIs.

- Automated Scraping: Uses Selenium with a headless Chrome driver to extract data from Google Maps.

- LLM Verification: Integrates with Ollama (Gemma 3:4b) to perform intelligent data extraction and classification from raw text.

- Parallel Processing: The Orchestrator uses asyncio and httpx to process multiple leads through the AI service simultaneously.

- Confidence Scoring: Automatically assigns a "HIGH", "MEDIUM", or "LOW" confidence level based on doctor titles, ratings, and contact availability.

# Tech Stack

- Language: Python 3.10

- Framework: FastAPI

- Automation: Selenium (Chrome)

- AI/ML: Ollama (Gemma 3)

- ontainerization: Docker & Docker Compose

- Data Handling: Pandas & Pydantic

# how to run
- download file
- run docker-compose up --build on CMD
- click on the link to download Ollama model locally https://ollama.com/ and install
- pull the model and open CMD and paste this command " ollama pull gemma3:4b "

# how to get api key
- for gemini visit https://aistudio.google.com/
- then below on the left choose get API KEYS
- copy the key and paste it on .env (a file which can be created and add the token inside to avoid exposing your token)

# Important note
I used Ollama locally because I consumed all the free tier token when testing for parrallel excution

<img width="767" height="233" alt="1" src="https://github.com/user-attachments/assets/5dabd7a9-52a3-4f6c-8d98-09256ea7a882" />

# Output results

<img width="972" height="151" alt="2" src="https://github.com/user-attachments/assets/b0be825d-ce2a-4266-b9a4-ca1b937db46f" />

