from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(documents)


def get_embedding():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_or_load_db(chunks, repo_name):

    persist_dir = f"chroma_db/{repo_name}"
    embedding = get_embedding()

    if chunks:
        print(f"Embedding {len(chunks)} chunks...")

        db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory=persist_dir
        )

        print("Embedding complete!")

    else:
        print("Loading existing DB...")
        db = Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding
        )

    return db