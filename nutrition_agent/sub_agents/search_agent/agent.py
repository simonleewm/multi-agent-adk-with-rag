from dotenv import load_dotenv
from google.adk.agents import Agent
import os

from google.adk.tools import VertexAiSearchTool, ToolContext

load_dotenv()

SEARCH_ENGINE_PATH = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global/collections/default_collection/engines/{os.getenv('SEARCH_ENGINE_ID')}"
nutrition_search_tool = VertexAiSearchTool(search_engine_id=SEARCH_ENGINE_PATH)

search_agent = Agent(
    name="search_agent",
    model=os.getenv("MODEL"),
    description="Specialist in searching the Australian Dietary Guidelines PDF for facts.",
    # Instructions focus specifically on its narrow domain
    instruction="""
    You are the Guidelines Researcher. Your job is to find facts within the 
    'Eat For Health' Australian Dietary Guidelines PDF using your search tool. 
    
    - When asked for targets, look for age and gender-specific 'kilojoule (kJ)' goals.
    - Identify the recommended 'serves per day' for the five food groups.
    - Always pass the extracted numbers back to the requester clearly.
    - Cite the specific section or page number if provided by the tool.
    """,
    tools=[nutrition_search_tool],
)
