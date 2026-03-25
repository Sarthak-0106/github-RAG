from repo_loader import clone_repo, load_repo_files
from vector_store import create_chunks, create_or_load_db
from rag_chain import get_llm, create_qa_chain
import os


repo_url = input("Enter GitHub repo URL: ")

repo_name = repo_url.split("/")[-1]

persist_path = f"chroma_db/{repo_name}"

chat_history = []

# Step 1: Check if DB exists
if os.path.exists(persist_path):
    print("Loading existing DB...")
    db = create_or_load_db(None, repo_name)

else:
    repo_path = clone_repo(repo_url)

    docs = load_repo_files(repo_path)

    chunks = create_chunks(docs)
    db = create_or_load_db(chunks, repo_name)

# Step 2: Create QA system
llm = get_llm()
qa_chain = create_qa_chain(llm, db)

# Step 3: Chat loop
while True:
    query = input("\nAsk a question (or 'exit'): ")

    if "project" in query.lower() or "about" in query.lower():
        query += " README overview architecture purpose"

    if query.lower() == "exit":
        break

    result = qa_chain.invoke({
        "question": query,
        "chat_history": chat_history
    })
    
    chat_history.append({
        "question": query,
        "answer": result
    })

    print("\nAnswer:\n", result)