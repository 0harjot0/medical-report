from llama_index.core.tools import FunctionTool
import google.generativeai as genai
from skills import diagnosis
from .prompts import PATIENT_RESEARCH_RETRIEVER
from llama_index.core.agent.react.base import ReActAgent
def create_patient_specific_analysis_agent(llm):
    """
    Analyzes patient-specific details and generates recommendations.
    """
    tools = [
        FunctionTool.from_defaults(diagnosis.search_drugs),
    ]
    
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        system_prompt=PATIENT_RESEARCH_RETRIEVER,
        verbose=True
    )
    
    return agent
