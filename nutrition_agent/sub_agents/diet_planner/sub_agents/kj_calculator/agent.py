import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from .tools import nutrition_calculator, check_daily_limit
from .....callback_logging import log_query_to_model, log_model_response

load_dotenv()

kj_calculator_agent = Agent(
    name="kj_calculator",
    model=os.getenv("MODEL"),
    description="Numerical specialist for energy conversions and limit checking.",
    instruction="""
    You are the Math Specialist. Your only job is to calculate energy values.
    
    1. Use 'nutrition_calculator' for converting kJ to Calories or vice versa.
    2. Use 'check_daily_limit' when provided with a current intake and a goal.
    3. If the Parent (Diet Planner) provides a target from the PDF, use it as the 'target_kj'.
    4. Provide the result back to the Parent Agent clearly.
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[nutrition_calculator, check_daily_limit]
)
