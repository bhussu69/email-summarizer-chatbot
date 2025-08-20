import os
import json
import base64
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import chromadb
from chromadb.utils import embedding_functions

# --- Config ---
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_PATH = "credentials.json"
TOKEN_PATH = "token.json"
SUMMARY_DIR = "summaries"
CHROMA_DB_DIR = "chroma_db"
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama2"
os.makedirs(SUMMARY_DIR, exist_ok=True)

# --- Gmail API ---
def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def fetch_unread_emails(n=5):
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", labelIds=["UNREAD"], maxResults=n).execute()
    messages = results.get("messages", [])
    emails = []
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"]).execute()
        snippet = msg.get("snippet", "")
        payload = msg.get("payload", {})
        headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
        raw_body = payload.get("body", {}).get("data")
        try:
            body = base64.urlsafe_b64decode(raw_body).decode("utf-8", errors="ignore") if raw_body else snippet
        except Exception:
            body = snippet
        emails.append({
            "id": m["id"],
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "body": body
        })
    return emails

# --- Olama streaming API handler ---
def olama_streaming_completion(prompt):
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt},
            timeout=120,
            stream=True
        )
        full_text = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    full_text += data.get("response", "")
                except json.JSONDecodeError:
                    continue
        if not full_text.strip():
            return "No response generated."
        return full_text.strip()
    except Exception:
        return "Error generating response."

# --- Email summarization ---
def summarize_email(email_text):
    prompt = (
        "You are an assistant that summarizes emails concisely in bullet points.\n"
        "Summarize this email:\n\n"
        + email_text
    )
    return olama_streaming_completion(prompt)

def summarize_all(summaries):
    combined_text = "\n".join(summaries)
    prompt = (
        "You are an assistant that generates a general summary from these bullet points.\n"
        "Summarize them concisely:\n\n"
        + combined_text
    )
    return olama_streaming_completion(prompt)

# --- ChromaDB vector store and semantic search ---
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
embedding_func = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(
    name="emails",
    embedding_function=embedding_func
)

def add_to_vector_store(email_id, text, summary):
    combined = text + "\nSummary:\n" + summary
    try:
        collection.add(
            documents=[combined],
            metadatas=[{"id": email_id}],
            ids=[email_id]
        )
    except Exception:
        pass  # silent fail on vector store errors

def semantic_search(query, k=5):
    try:
        results = collection.query(query_texts=[query], n_results=k)
        return results
    except Exception:
        return {"documents": [[]], "metadatas": [[]]}

# --- AI-powered chat loop ---
def ai_chat_loop():
    print("\n🤖 Ask anything about your emails (type 'exit' to quit):")
    while True:
        q = input("You: ").strip()
        if q.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        results = semantic_search(q, k=5)
        docs = results.get("documents", [[]])[0]
        if not docs:
            print("No relevant emails found.")
            continue
        context = "\n\n---\n\n".join(docs)
        prompt = (
            "Given the following email contents, answer the question succinctly:\n\n"
            f"{context}\n\nQuestion: {q}\nAnswer:"
        )
        answer = olama_streaming_completion(prompt)
        print(f"\n🤖 {answer}\n")

# --- Main entry point ---
def main():
    try:
        n = int(input("Enter how many top unread emails to summarize: "))
    except ValueError:
        print("Invalid input, must be an integer.")
        return
    emails = fetch_unread_emails(n)
    if not emails:
        print("No unread emails found.")
        return
    all_summaries = []
    for email in emails:
        summary = summarize_email(email["body"])
        add_to_vector_store(email["id"], email["body"], summary)
        all_summaries.append(summary)
        print(f"\n📌 Email '{email['subject']}' summary:\n{summary}\n")
    general_summary = summarize_all(all_summaries)
    print("\n📊 General Summary:\n", general_summary)
    ai_chat_loop()

if __name__ == "__main__":
    main()
