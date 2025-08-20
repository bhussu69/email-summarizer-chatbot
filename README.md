# Gmail CLI AI ChatBot

A powerful, terminal-based AI assistant that securely accesses your Gmail inbox, summarizes unread emails using a local LLaMA2 model via Olama API, and enables interactive, natural language querying of your email content through semantic search powered by ChromaDB and dynamic LLM-generated responses.

---

## Features

- **Secure OAuth2 authentication** with Gmail API  
- **Fetch and summarize** top unread emails in concise bullet points  
- **Store email content and summaries** as embeddings in ChromaDB for efficient semantic retrieval  
- **Intelligent chat interface** for asking detailed questions about your emails  
- **Fully local deployment**, ensuring privacy and control—no cloud AI services required

---

## Prerequisites

- Python 3.11 or later  
- [Olama CLI](https://olama.ai/) installed with LLaMA2 model  
- Active Google Cloud project with Gmail API enabled and OAuth2 credentials (`credentials.json`)  

---

## Installation

1. **Clone the repository**

git clone <your-repo-url>
cd <repo-folder>

text

2. **Create and activate a virtual environment (recommended)**

python3 -m venv venv
source venv/bin/activate

text

3. **Install dependencies**

pip install -r requirements.txt

text

4. **Add Gmail OAuth2 credentials**

- Follow Google's guide to create OAuth 2.0 credentials for a desktop application in your Google Cloud Console  
- Download the `credentials.json` file  
- Place it in the project root directory  
- *Important:* Never commit or share this file publicly  

5. **Download and run Olama LLaMA2 model locally**

olama pull llama2
olama run llama2

text

---

## Usage

Run the bot with:

PYTHONPATH=$(pwd) python email_bot.py

text

- Enter the number of unread emails you want to summarize  
- Review the individual email summaries and the general summary provided  
- Enter the interactive chat mode that lets you ask natural language questions about your emails  
- Type `exit` or `quit` to close the chat session

---

## Project Structure

/
├── email_bot.py # Core CLI program with all bot functionality
├── requirements.txt # Python dependencies
├── credentials.json # OAuth2 credentials (user-provided, ignored by Git)
├── token.json # OAuth2 token cache (auto-generated, ignored by Git)
├── chroma_db/ # Vector embeddings storage (auto-generated)
├── summaries/ # Cached email summaries (auto-generated)
└── .gitignore # Ignores sensitive and cache files

text

---

## Security & Privacy

- OAuth2 credentials and tokens **must never be committed** to source control  
- All AI inference runs **locally** on your machine through Olama’s LLaMA2 model, guaranteeing data privacy  
- Your vector embeddings and cached summaries are stored only on your machine

---

## Troubleshooting

- **Authentication issues:** Delete `token.json` to reset Gmail authorization  
- **No responses or failures:** Verify that your Olama LLaMA2 server is running and accessible at [http://localhost:11434/api/generate](http://localhost:11434/api/generate)  
- **File permission errors:** Ensure the project folders (`chroma_db/` and `summaries/`) have proper read/write permissions

---

## Contribution & License

This project is open source under the MIT License. Contributions, improvements, and bug reports are welcome via GitHub.

---

## Acknowledgments

- Gmail API powered by Google  
- Olama LLaMA2 for local LLM inference  
- ChromaDB for vector similarity search

---

Thank you for using this project! Your privacy-first AI assistant for Gmail awaits.
