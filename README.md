# LangChain + LangSmith Observability Demo

A tiny, runnable project that shows **tracing, nested spans, dashboards, and feedback** in LangSmith using both an LCEL chain and an Agent with tools.

## 1) Setup

1. Python 3.11+ recommended
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set keys:
   - `OPENAI_API_KEY`
   - `LANGCHAIN_TRACING_V2=true`
   - `LANGCHAIN_API_KEY` (aka LangSmith API key)
   - `LANGCHAIN_PROJECT=langsmith-demo`

   > Docs on tracing & env vars: see LangSmith quickstart and LangChain/LangServe notes.


## 2) Run the examples

### Basic LCEL chain (single span)
```bash
python app/chain_basic.py
```

### Zero‑shot Agent with tools (nested spans for tool calls)
```bash
python app/agent_zero_shot.py
```

### (Optional) LangServe with inline feedback buttons
```bash
uvicorn app.langserve_app:app --reload --port 8000
# Open http://localhost:8000/chain/playground
# Use 👍/👎 to send feedback; click 'Create public trace' to copy a shareable link.
```

## 3) What to look for in LangSmith

1. **Projects & Traces**: Open your project (`LANGCHAIN_PROJECT`) and confirm new runs appear with tags `demo`, `lcel`, `agent`, etc.  
2. **Nested spans**: For the agent example, expand the run to see tool spans under the parent agent span.  
3. **Metadata filters**: We tag runs with `environment=local`. Filter by metadata in the UI or via the SDK.  
4. **Dashboards**: Go to **Monitoring → Dashboards** to see prebuilt charts for token usage, error rates, latency, etc.  
5. **Feedback**: In `tests/test_tracing.py` we log inputs/outputs and a reference expectation inside `with trace_feedback()`. You can also submit thumbs‑up/down from the LangServe playground.  
6. **Datasets**: Convert interesting traces into dataset examples to regression‑test improvements later.

## 4) Useful snippets

### Filter runs (Python)
```python
from langsmith import Client
client = Client()
for r in client.list_runs(project_name="langsmith-demo", filter="and(eq(metadata_key,'environment'),eq(metadata_value,'local'))"):
    print(r.id, r.run_type, r.name, r.latency_ms)
```

## 5) Troubleshooting
- No traces? Ensure `.env` is loaded and `LANGCHAIN_TRACING_V2=true`, `LANGCHAIN_API_KEY` are set **in the same shell**.
- Wrong project? Set `LANGCHAIN_PROJECT`.
- Corporate proxy blocks: set `HTTPS_PROXY`/`HTTP_PROXY` if needed.
- For selective tracing, you can use `langsmith.tracing_context()` to enable/disable without env vars.

## 6) References
- Trace with LangChain: https://docs.smith.langchain.com/observability/how_to_guides/trace_with_langchain
- Observability quick start: https://docs.smith.langchain.com/observability
- Dashboards: https://docs.smith.langchain.com/observability/how_to_guides/dashboards
- Log user feedback: https://docs.smith.langchain.com/evaluation/how_to_guides/attach_user_feedback
- Query traces / export: https://docs.smith.langchain.com/observability/how_to_guides/export_traces
- LangServe feedback buttons & env vars: https://python.langchain.com/docs/langserve/
