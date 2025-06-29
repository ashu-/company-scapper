from crewai import Agent, Task, tool

from crewai_tools import GoogleSearch
from crewai_llm import LLM

llm_groq = LLM(
    model="groq/groq-llama-3.2-70b-instruct"
    api_key=os.getenv("GROQ_API_KEY")
)


@tool
def google_search(query: str) -> str:
    return GoogleSearch().search(query)

agent = Agent(
    llm=llm_groq,
    tools=[google_search],
    max_iterations=3,
    verbose=True,
    role="Content Explorer",
    description="You are a content explorer. Your task is to explore the content of a website and extract the most relevant information."
    
)
