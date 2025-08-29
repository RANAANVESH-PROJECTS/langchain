from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.schema.runnable import RunnableSequence, RunnableParallel
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Define LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)


# ---- Define Tools ----
@tool
def research_tool(topic: str) -> str:
    """Research a given topic and return findings."""
    print("Researching on topic:", topic)
    prompt = PromptTemplate.from_template("Research about: {topic}")
    formatted_prompt = prompt.format(topic=topic)
    return llm.invoke(formatted_prompt).content

@tool
def outline_tool(research: str) -> str:
    """Generate a detailed outline based on research text."""
    print("Generating Outline...")
    prompt = PromptTemplate.from_template(
        "Create a detailed outline based on this research:\n\n{research}"
    )
    formatted_prompt = prompt.format(research=research)
    return llm.invoke(formatted_prompt).content

@tool
def summary_tool(research: str) -> str:
    """Summarize the research text into key points."""
    print("Summarizing Research...")
    prompt = PromptTemplate.from_template(
        "Summarize this research into concise bullet points:\n\n{research}"
    )
    formatted_prompt = prompt.format(research=research)
    return llm.invoke(formatted_prompt).content


# ---- Build Pipeline with Parallel Branches ----
pipeline = RunnableSequence(
    {
        # Run research first
        "research": research_tool,
    }
    | RunnableParallel(
        {
            # Branch 1: Outline -> Article
            "article": RunnableSequence(
                lambda x: x["research"],  # extract research
                outline_tool,
            ),
            # Branch 2: Summary directly from research
            "summary": RunnableSequence(
                lambda x: x["research"],
                summary_tool,
            ),
        }
    )
)


# ---- Run ----
if __name__ == "__main__":
    topic = "Impact of AI in Education"
    result = pipeline.invoke(topic)

    print("\n\n=== Results ===\n")
    print("Summary:\n", result["summary"])
    print("\nArticle:\n", result["article"])