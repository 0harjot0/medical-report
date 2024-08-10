from utils import create_pdf
from logger import setup_logging
import os
from dotenv import load_dotenv
from llama_index.core.tools.query_engine import QueryEngineTool
from llama_index.core.query_engine import SubQuestionQueryEngine
from agents.data_retrieval import create_medical_data_retrieval_agent
from agents.patient_specifics import create_patient_specific_analysis_agent
from llama_index.core.agent.react.base import ReActAgent
from llama_index.llms.gemini import Gemini

from openai import OpenAI

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = Gemini(model='models/gemini-1.5-flash', api_key=GOOGLE_API_KEY)

def create_medical_agent():
    
    data_retrieval_tool = QueryEngineTool.from_defaults(
        create_medical_data_retrieval_agent(llm),
        name="medical_data_retrieval_agent",
        description="""
        Gathers and synthesizes recent medical literature, clinical guidelines, epidemiological data, and treatment outcomes to provide a comprehensive summary. This summary will inform the creation of detailed medical reports.
        """
    )

    
    patient_analysis_tool = QueryEngineTool.from_defaults(
        create_patient_specific_analysis_agent(llm),
        name="patient_specific_analysis_agent",
        description="""
            Analyzes the patient's medical history, symptoms, test results, and other details to assess their condition, recommend diagnostic tests, suggest treatment options, and estimate prognosis. Provides personalized insights for effective diagnosis and treatment.
        """
    )


    orchestrator_agent = ReActAgent.from_tools(
        [data_retrieval_tool, patient_analysis_tool],
        system_prompt="""
        The medical report orchestrator agent is responsible for managing the overall workflow and coordination of the medical data retrieval and patient-specific analysis agents.
        It will:
        - Orchestrates the workflow and integration of the medical data retrieval and patient-specific analysis.
        - Ensure smooth communication and integration of the information gathered by the two agents
        - Synthesize the findings from the data retrieval and patient analysis into a comprehensive medical report
        - Oversee the entire process to ensure accurate completion of the medical report
        """,
        llm=llm,
        verbose=True
    )
    return orchestrator_agent

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("The logging has started!!!")
    
    agent = create_medical_agent()
    

 
    
    response = agent.query(
        """
        write a report on latest articles on cholera. 
        """
    )

    print(response)
    
    # Create a PDF from the response
    create_pdf(str(response))
    # create_pdf("# Test\nThis is a test.")