from langchain_openai import ChatOpenAI
from config import HF_TOKEN
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_llm():
    return ChatOpenAI(
        model="meta-llama/Llama-3.1-8B-Instruct:novita",
        api_key=HF_TOKEN,
        base_url="https://router.huggingface.co/v1"
    )

def create_qa_chain(llm, vector_store):

    retriever = vector_store.as_retriever(search_kwargs={"k": 10})

    prompt = ChatPromptTemplate.from_template("""
    You are an expert software engineer analyzing a GitHub repository.

    Use ONLY the provided context.

    Rules:
    - You may infer high-level purpose ONLY if there are strong signals (file names, README, structure)
    - DO NOT invent features or functionality not supported by context
    - If unsure, say: "Based on the available code, it appears that..."
    - If no useful info exists, say: "I could not find enough information in the codebase."

    Always include:
    - File names when relevant
    - Function/class names when relevant

    Context:
    {context}

    Question:
    {question}

    Answer:
    """)
    
    # def format_docs(docs):
    #     return "\n\n".join(doc.page_content for doc in docs)

    def format_docs(docs):
    # PRIORITY SORT
        docs = sorted(
            docs,
            key=lambda x: x.metadata.get("priority", 1),
            reverse=True
        )

        return "\n\n".join(
            f"[FILE: {doc.metadata.get('source')}]\n{doc.page_content}"
            for doc in docs
        )

    chain = (
        {
            "context": retriever | format_docs,
            "question": lambda x: x
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain