from dotenv import load_dotenv
import google.auth
from google.adk.agents import Agent
from google.adk.tools import AgentTool
import google.cloud.logging
import os

from .callback_logging import log_query_to_model, log_model_response

from .sub_agents.diet_planner.agent import diet_planner
from .sub_agents.search_agent.agent import search_agent


# Load env
load_dotenv()

# Configure logging to the Cloud
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

root_agent = Agent(
    name="nutrition_coach",
    model=os.getenv("MODEL"),
    description="A friendly Australian Nutrition Coach that manages diet planning and research.",
    # The instruction tells the Root Agent how to delegate
    instruction="""
    You are the head Australian Nutrition Coach. Your job is to coordinate the user's journey.

    1. Confirm from the user their gender and age, if not provided.
    2. If the user wants to search for nutrition factual data, RDI, kJ targets, serve sizes, or specific guidelines from the official Australian Dietary Guideline: 'Eat For Health' PDF, delegate to the 'search_agent'. 
    3. If the user wants to create a meal plan or needs nutritional analysis of their food, delegate to the 'diet_planner'. 
       Only for analysing what a user has already eaten or creating meal plan; does NOT know official guidelines; must receive them from 'nutrition_coach'
    4. Always ensure the tone is encouraging and uses Australian English (e.g., 'G'day', 'kJ' instead of 'Calories').
    5. When a sub-agent returns information, do not narrate what you are about to do next. Process the data internally and move immediately to the next tool call or the final response.
    6. Analyse the user's prompt and determine all required sub-agents (Search, Planner, Calculator) immediately. Execute them in sequence without conversational filler between calls.
    
    Once a sub-agent provides data, summarise it clearly for the user.
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    sub_agents=[diet_planner],
    tools=[
        AgentTool(agent=search_agent, skip_summarization=False),
    ],
)
