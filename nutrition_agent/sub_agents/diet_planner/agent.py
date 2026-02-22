import os
from dotenv import load_dotenv
from google.adk.agents import Agent
# Import the specialized sub-sub-agent
from .sub_agents.kj_calculator.agent import kj_calculator_agent

load_dotenv()

diet_planner = Agent(
    name="diet_planner",
    model=os.getenv("MODEL"),
    # Instruction defines the "Middle Manager" role
    instruction="""
    You are the Senior Diet Planner. Your goal is to turn raw user food data 
    into a structured plan.
    
    1. Receive user intake or goals from the Root Coach.
    2. If you need to verify if an intake is within a specific energy limit, 
       delegate the math to the 'kj_calculator'.
    3. Use the results from the calculator to provide a 'Go/No-Go' recommendation 
       for the user's current diet.
    4. Do not perform kJ-to-Calorie or Calorie-to-kJ math yourself,
       delegate all numerical energy conversions to the 'kj_calculator' tool.
    5. Organize the final output into a clear daily plan format.
    """,
    # Registering the next level in the hierarchy
    sub_agents=[kj_calculator_agent]
)
