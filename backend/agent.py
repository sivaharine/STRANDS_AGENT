from strands import Agent
from strands.models.bedrock import BedrockModel

from tools.weather_tool import get_weather
from tools.calculator_tool import calculate
from tools.web_search_tool import web_search
from tools.database_tool import query_database

from config import BEDROCK_MODEL_ID, AWS_REGION


model = BedrockModel(
    model_id=BEDROCK_MODEL_ID,
    
)

agent = Agent(
    model=model,
    tools=[
        get_weather,
        calculate,
        web_search,
        query_database
    ]
)


async def run_agent(prompt):

    response = agent(prompt)

    return response