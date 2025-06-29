from crewai import Agent, Task, Crew
from crewai.tools import tool
from crewai.llm import LLM
from dotenv import load_dotenv
load_dotenv(override=True)
from datetime import datetime
now = datetime.now()

today = now.strftime('%d-%m-%Y')
print(today)

import requests

chat_groq = LLM(model='groq/llama-3.3-70b-versatile')

@tool('serpa search tool')
def get_serpa_search_data(search_query:str):
    """return google search using search query provided"""
    import http.client
    import json
    
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
      "q": search_query
    })
    serpa_api_key = os.getenv("SERPA_API_KEY")
    headers = {
      'X-API-KEY': serpa_api_key,
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    search_data = data.decode("utf-8")
    print(search_data)
    return search_data

search_agent = Agent(llm=chat_groq,
                     role="Content Explorer",
                     tools=[get_serpa_search_data],
                     backstory="You are a content explorer . get latest information , latest news, interesting data for company name provided in  {search_query) provided.",
                     goal="get latest information , latest news, interesting data for company name provided {search_query) provided.",
                     max_iter=2,cache=True
                    ) 
search_task = Task(agent=search_agent,
                   expected_output="based on provided {search_query} you need to provide latest information , latest news, interesting data",
                   description="call tool with {search_query} as argument and provide latest information , latest news, interesting data using search")
Script_Writer = Agent (
    role = 'Company Analyzer writter',
    goal = 'With the details given to you. analyze and write a good analysis about the company provided in {search_query}. latest investments, latest product launch ',
    llm=chat_groq,
    verbose = True,
    backstory = ('You are an expert company analyzer and provide report like economic times. You are very good in analyzing and writing company info\
                 Tell as a company analysis in 200 words.\
                 Consider you are on '+today),
)

create_a_analysis = Task (
                      description = "Considering the given details in time order make provide a complete company news and data",
                      expected_output = "A good company analysis",
                      agent = Script_Writer,
                      context = [search_task],
                      output_file = 'Script.txt'
                    )
from crewai import Crew, Process
from datetime import datetime

# Callback function to print a timestamp
def timestamp(Input):
    print(datetime.now())

# Define the crew with agents and tasks in sequential process

# result = crew.kickoff (inputs={'search_query' : "sARLA aVIATION https://www.sarla-aviation.com/"})

def get_company_info(search_query):
    crew = Crew (
    agents = [search_agent, Script_Writer],
    tasks = [search_task, create_a_analysis],
    verbose = True,
    Process = Process.sequential,
    step_callback = timestamp
    )
    result = crew.kickoff(inputs={'search_query' : search_query})
    
    # Convert CrewOutput to a string to make it JSON serializable
    print(result)
    return str(result)