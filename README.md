# LangChain Concepts

Examples on Langchain Concepts

## 1) Setup

1. Python 3.11+ recommended
2. `pip install -r requirements.txt`
3. Set the following Keys in .env file:
   - `OPENAI_API_KEY`
   - `LANGCHAIN_TRACING_V2=true`
   - `LANGCHAIN_API_KEY` (aka LangSmith API key)
   - `LANGCHAIN_PROJECT=langsmith-demo`

   > Docs on tracing & env vars: see LangSmith quickstart and LangChain/LangServe notes.


## 2) Run the examples by running each file

### Basic LCEL chain (single span)
```bash
langchain/basic_chaining.py
```
