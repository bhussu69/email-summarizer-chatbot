# Gmail CLI AI ChatBot

A terminal-based AI-powered Gmail assistant that securely fetches unread emails via Gmail API, summarizes them using a local LLaMA2 model through Olama API with streaming JSON handling, stores email texts and summaries as embeddings in ChromaDB for semantic search, and provides an interactive command-line chat interface that answers natural language questions by retrieving relevant emails via semantic search and generating dynamic responses using the LLaMA2 model.

## Requirements

- Python 3.11+  
- Olama CLI with LLaMA2 model running locally (`olama run llama2`)  
- Gmail OAuth2 credentials JSON file (`credentials.json`)

## Setup and Run

1. Clone the repo:

git clone <your-repo-url>
cd <repo-folder>

text

2. Install dependencies:

pip install -r requirements.txt

text

3. Place your `credentials.json` (Gmail OAuth2 desktop app credentials) in the project root.

4. Start Olama LLaMA2 server:

olama pull llama2
olama run llama2

text

5. Run the chatbot:

PYTHONPATH=$(pwd) python email_bot.py

text

6. Input the number of unread emails to summarize, then ask questions interactively.

## Features

- Fetches unread emails and generates bullet summaries  
- Stores email contents and summaries as vector embeddings  
- Semantic search for relevant emails on user questions  
- Dynamic AI-generated answers based on retrieved emails and user query  
- Full streaming support and silent error handling (no raw JSON errors shown)  
- Easy setup with OAuth2 and fully local AI inference  

## Project Structure

- `email_bot.py` — main script combining all logic  
- `requirements.txt` — dependency list  
- `credentials.json` — Gmail OAuth2 credentials (user must add)  
- `token.json` — OAuth token (auto-generated)  
- `chroma_db/` — local vector database (auto-generated)  
- `summaries/` — cache of email summaries (auto-generated)  

## Security

- Never commit credentials or tokens—`.gitignore` keeps `credentials.json`, `token.json`, and data folders out of Git  
- Users provide their own OAuth credentials securely

## Troubleshooting

- Delete `token.json` to reset Gmail auth if needed  
- Ensure Olama server is running and reachable at `http://localhost:11434/api/generate`  
- Check folder permissions if vector search fails

---

Feel free to contribute or create issues on GitHub!
