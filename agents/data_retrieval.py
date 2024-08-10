from llama_index.core.tools import FunctionTool
import google.generativeai as genai

from skills import latest_medical_research
from .prompts import INFO_RETRIEVER
from skills import get_medical_articles_full_text 
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.agent.legacy.react.base import ReActAgent

def create_medical_data_retrieval_agent(llm):
    """
    Retrieves and analyzes relevant medical data for generating a report.
    """
    tools = [
        FunctionTool.from_defaults(latest_medical_research),
        FunctionTool.from_defaults(get_medical_articles_full_text),
    ]
    
    agent = ReActAgent.from_tools(tools=tools, llm=llm, system_prompt=INFO_RETRIEVER, 
                                  verbose=True) 
    
    return agent
