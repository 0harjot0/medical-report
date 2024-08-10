import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def create_medical_literature_tool(model):
    def medical_literature_analysis(query):
        prompt = f"""
        You are a medical research expert. Analyze recent medical literature related to: {query}
        
        Provide a summary covering:
        1. Key findings from recent studies
        2. Emerging trends in research
        3. Potential implications for clinical practice
        
        Base your analysis on the most current and reputable medical journals and publications.
        """
        response = model.generate_content(prompt)
        return response.text
    
    return medical_literature_analysis

def create_guideline_summary_tool(model):
    def guideline_summary(condition):
        prompt = f"""
        You are a medical guidelines expert. Summarize the current clinical guidelines for: {condition}
        
        Include:
        1. Diagnostic criteria
        2. Recommended treatment approaches
        3. Any recent updates or changes to the guidelines
        4. Source of the guidelines (e.g., WHO, CDC, specialty medical associations)
        
        Ensure the information is up-to-date and from authoritative sources.
        """
        response = model.generate_content(prompt)
        return response.text
    
    return guideline_summary

def create_treatment_recommendation_tool(model):
    def treatment_recommendation(condition, patient_details):
        prompt = f"""
        You are a medical treatment specialist. Recommend treatment options for:
        Condition: {condition}
        Patient Details: {patient_details}
        
        Provide:
        1. First-line treatment options
        2. Alternative treatments if applicable
        3. Lifestyle modifications
        4. Potential side effects and precautions
        
        Base your recommendations on current best practices and consider the patient's specific circumstances.
        """
        response = model.generate_content(prompt)
        return response.text
    
    return treatment_recommendation

def create_epidemiology_tool(model):
    def epidemiology_analysis(condition):
        prompt = f"""
        You are an epidemiology expert. Provide an epidemiological overview of: {condition}
        
        Include:
        1. Prevalence and incidence rates
        2. Demographic distribution
        3. Known risk factors
        4. Trends over time
        5. Geographic variations if applicable
        
        Use the most recent and reliable epidemiological data available.
        """
        response = model.generate_content(prompt)
        return response.text
    
    return epidemiology_analysis

def create_patient_outcomes_tool(model):
    def patient_outcomes_analysis(condition, treatment):
        prompt = f"""
        You are a medical outcomes researcher. Analyze patient outcomes for:
        Condition: {condition}
        Treatment: {treatment}
        
        Provide information on:
        1. Treatment efficacy rates
        2. Long-term prognosis
        3. Quality of life implications
        4. Factors influencing outcomes
        5. Comparison with alternative treatments if applicable
        
        Base your analysis on recent clinical studies and reliable medical databases.
        """
        response = model.generate_content(prompt)
        return response.text
    
    return patient_outcomes_analysis

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Create tools
literature_tool = create_medical_literature_tool(model)
guideline_tool = create_guideline_summary_tool(model)
treatment_tool = create_treatment_recommendation_tool(model)
epidemiology_tool = create_epidemiology_tool(model)
outcomes_tool = create_patient_outcomes_tool(model)

# Example usage
condition = "Type 2 Diabetes"
literature_analysis = literature_tool(condition)
guideline_summary = guideline_tool(condition)
treatment_recommendation = treatment_tool(condition, "55-year-old male, overweight, hypertensive")
epidemiology_data = epidemiology_tool(condition)
outcomes_analysis = outcomes_tool(condition, "Metformin")

# Print results
print("Literature Analysis:", literature_analysis)
print("\nGuideline Summary:", guideline_summary)
print("\nTreatment Recommendation:", treatment_recommendation)
print("\nEpidemiology Data:", epidemiology_data)
print("\nOutcomes Analysis:", outcomes_analysis)



//detailed prompts

def create_medical_literature_tool(model):
   
    # Tool for gathering and analyzing medical literature
    literature_tool = QueryEngineTool.from_defaults(
        create_medical_literature_agent(model),
        name="medical_literature_agent",
        description="""
        Retrieves and analyzes recent medical literature related to specific diseases and medical conditions.
        Provides a summary covering key findings from recent studies, emerging trends in research, and potential implications for clinical practice.
        Bases the analysis on the most current and reputable medical journals and publications.
        """
    )

    # Tool for summarizing medical guidelines
    guideline_tool = QueryEngineTool.from_defaults(
        create_guideline_summary_agent(model),
        name="guideline_summary_agent",
        description="""
        Summarizes the current clinical guidelines for specific medical conditions.
        Includes diagnostic criteria, recommended treatment approaches, recent updates or changes to the guidelines, and sources of the guidelines (e.g., WHO, CDC, specialty medical associations).
        Ensures the information is up-to-date and from authoritative sources.
        """
    )

    # Tool for recommending treatments
    treatment_tool = QueryEngineTool.from_defaults(
        create_treatment_recommendation_agent(model),
        name="treatment_recommendation_agent",
        description="""
        Recommends treatment options for specific medical conditions, taking into account patient details.
        Provides first-line treatment options, alternative treatments if applicable, lifestyle modifications, and potential side effects and precautions.
        Bases recommendations on current best practices and considers the patient's specific circumstances.
        """
    )

    # Tool for analyzing epidemiological data
    epidemiology_tool = QueryEngineTool.from_defaults(
        create_epidemiology_agent(model),
        name="epidemiology_agent",
        description="""
        Provides an epidemiological overview of specific medical conditions.
        Includes prevalence and incidence rates, demographic distribution, known risk factors, trends over time, and geographic variations if applicable.
        Uses the most recent and reliable epidemiological data available.
        """
    )

    # Tool for analyzing patient outcomes
    outcomes_tool = QueryEngineTool.from_defaults(
        create_patient_outcomes_agent(model),
        name="patient_outcomes_agent",
        description="""
        Analyzes patient outcomes for specific medical conditions and treatments.
        Provides information on treatment efficacy rates, long-term prognosis, quality of life implications, factors influencing outcomes, and comparison with alternative treatments if applicable.
        Bases the analysis on recent clinical studies and reliable medical databases.
        """
    )
