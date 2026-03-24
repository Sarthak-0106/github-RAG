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

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_template("""
    You are a codebase assistant.

    Answer ONLY from the provided context.
    Do NOT guess or infer.

    If the answer is not clearly present, say:
    "I could not find this in the codebase."

    Always include:
    - File name
    - Function/Class name (if available)

    Context:
    {context}

    Question:
    {question}

    Answer:
    """)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

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