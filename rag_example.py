# pdf_rag_questions_only.py
# pip install -U langchain langchain-openai langchain-community langchain-text-splitters chromadb python-dotenv pypdf

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import initialize_agent, AgentType, tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

load_dotenv()

PDF_PATH = "sample_sachin_bio.pdf"  # update with absolute path if needed

# --- Load + index PDF once ---
pages = PyPDFLoader(PDF_PATH).load()
splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=120)
chunks = splitter.split_documents(pages)

emb = OpenAIEmbeddings()
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=emb,
    collection_name="sachin_bio_demo",
    # persist_directory="chroma_db_sachin"  # uncomment for persistence
)

# --- Retriever tool ---
@tool
def retrieve(query: str) -> str:
    """Retrieve top passages from the Sachin biography PDF; returns text with sources."""
    hits = vectordb.similarity_search(query, k=4)
    return "\n".join(f"[{h.metadata.get('source','?')}] {h.page_content}" for h in hits)

# --- Agent ---
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = initialize_agent(
    tools=[retrieve],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

if __name__ == "__main__":
    print("\n--- Ask Questions about Sachin Tendulkar's Biography PDF ---\n")
    while True:
        q = input("Your question (or 'q' to quit): ").strip()
        if q.lower() == "q":
            break
        out = agent.invoke({"input": q})
        print("\nAnswer:\n", out["output"], "\n")
