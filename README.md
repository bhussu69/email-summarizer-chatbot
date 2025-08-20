# Gmail CLI AI ChatBot

A terminal-based AI-powered Gmail assistant that securely fetches unread emails via Gmail API, summarizes them using a local LLaMA2 model through Olama API with streaming JSON handling, stores email texts and summaries as embeddings in ChromaDB for semantic search, and provides an interactive command-line chat interface that answers natural language questions by retrieving relevant emails via semantic search and generating dynamic responses using the LLaMA2 model.

---

## Requirements

- **Python 3.11+**  
- **Olama CLI** with LLaMA2 model running locally (`olama run llama2`)  
- **Gmail OAuth2 credentials JSON** file (`credentials.json`)

---

## Setup and Run

1. Clone the repository and enter folder

git clone <your-repo-url>
cd <repo-folder>
2. Install Python dependencies

pip install -r requirements.txt
3. Place your Gmail OAuth2 credentials JSON as credentials.json in the project root
4. Pull and run Olama LLaMA2 locally

olama pull llama2
olama run llama2
5. Run the chatbot CLI

PYTHONPATH=$(pwd) python email_bot.py

text

---

## How It Works

1. **Fetch & Summarize Emails**

emails = fetch_unread_emails(n)
for email in emails:
summary = summarize_email(email["body"])
add_to_vector_store(email["id"], email["body"], summary)
print(f"Email: {email['subject']}\nSummary: {summary}\n")

text

2. **General Summary**

general_summary = summarize_all(all_summaries)
print(f"General Summary:\n{general_summary}")

text

3. **Interactive AI Chat**

def ai_chat_loop():
while True:
query = input("You: ").strip()
if query.lower() in ["exit", "quit"]:
break

text
    results = semantic_search(query, k=5)
    docs = results.get("documents", [[]])

    if not docs:
        print("No relevant emails found.")
        continue

    context = "\n\n---\n\n".join(docs)
    prompt = f"Using the emails below, answer:\n{context}\n\nQuestion: {query}\nAnswer:"

    answer = olama_streaming_completion(prompt)
    print(f"\n🤖 {answer}\n")

text

---

## Project Structure

.
├── email_bot.py # Main script (all functionality)
├── requirements.txt # Python packages
├── credentials.json # Gmail OAuth2 (user adds this)
├── token.json # OAuth token (auto-generated)
├── chroma_db/ # Vector database storage folder
├── summaries/ # Cached email summaries
├── .gitignore # Security exclusions (ignore credentials, tokens, etc.)

text

---

## Security Best Practices

- **Never push your `credentials.json` or `token.json` to public repos**  
- `.gitignore` ensures sensitive files are excluded  
- Users must create and add their own OAuth credentials securely  

---

## Troubleshooting

- Delete `token.json` to reset Gmail authentication  
- Confirm Olama LLaMA2 server is running and accessible at `http://localhost:11434/api/generate`  
- Verify directory permissions for `chroma_db` and `summaries`

---

## License & Contribution

This project is open source under the MIT License. Contributions, feedback, and issues are welcome on GitHub.

---

Made with ❤️ using Google Gmail API, Olama local LLaMA2, and ChromaDB.
