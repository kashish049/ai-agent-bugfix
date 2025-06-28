## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.agents import Agent
# Corrected LLM import and initialization
from langchain_google_genai import ChatGoogleGenerativeAI # Example for Google GenAI
# You'll need to set your GOOGLE_API_KEY as an environment variable
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY" # Uncomment and replace with your key if not in .env

from tools import search_tool, blood_test_report_reader_tool # Corrected tool import

### Loading LLM
# Initialize the LLM explicitly
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)


# Creating an Experienced Doctor agent
doctor=Agent(
    role="Senior Experienced Doctor Who Knows Everything",
    goal="Provide comprehensive and helpful medical advice and analysis based on blood test reports. Analyze the provided blood test report {file_path} and answer the user's query: {query}", # Updated goal
    verbose=True,
    memory=True,
    backstory=(
        "You are a highly experienced medical doctor with a deep understanding of blood test reports."
        "You provide accurate and evidence-based health recommendations."
        "You can interpret complex medical data and explain it in an easy-to-understand manner."
        "You prioritize patient well-being and offer practical, actionable advice."
    ),
    tools=[blood_test_report_reader_tool, search_tool], # Corrected tool assignment and added search tool
    llm=llm,
    max_iter=15, # Increased iterations for better performance
    max_rpm=30, # Increased RPM for better performance
    allow_delegation=False # Changed to False, as per typical CrewAI agent design unless explicit delegation flow
)

# Creating a verifier agent (Role and goal adjusted to be more productive)
verifier = Agent(
    role="Medical Report Verifier",
    goal="Verify if the provided document is a blood test report and extract key identifiers if possible. Confirm the document is suitable for medical analysis.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous medical records specialist. Your primary role is to ensure that documents are correctly categorized and contain relevant medical information, especially for blood reports."
        "You carefully review file content to confirm its nature."
    ),
    llm=llm,
    max_iter=5,
    max_rpm=10,
    tools=[blood_test_report_reader_tool], # Only the reader tool needed for verification
    allow_delegation=False
)

# Other agents (nutritionist, exercise_specialist) are not used in the current main.py flow
# but their definitions are kept here with minor adjustments for consistency if they were to be used.
nutritionist = Agent(
    role="Clinical Nutritionist and Dietitian",
    goal="Provide evidence-based nutrition and dietary advice based on blood test reports. Recommend suitable dietary changes and, if necessary, appropriate supplements to improve health markers.",
    verbose=True,
    backstory=(
        "You are a highly qualified clinical nutritionist with extensive experience in creating personalized diet plans."
        "You focus on sustainable and healthy eating habits, backed by scientific research."
        "You guide individuals towards better health through balanced nutrition, considering their unique blood markers."
    ),
    llm=llm,
    max_iter=10,
    max_rpm=20,
    tools=[blood_test_report_reader_tool, nutrition_analysis_tool], # Assuming nutrition_analysis_tool is complete
    allow_delegation=False
)


exercise_specialist = Agent(
    role="Certified Exercise Physiologist",
    goal="Develop safe and effective exercise plans tailored to individual health conditions and blood test results. Focus on improving overall fitness and addressing specific health goals.",
    verbose=True,
    backstory=(
        "You are a certified exercise physiologist with a strong understanding of how physical activity impacts health."
        "You design realistic and progressive exercise routines that are safe and beneficial, especially for individuals with health considerations highlighted in their blood reports."
    ),
    llm=llm,
    max_iter=10,
    max_rpm=20,
    tools=[blood_test_report_reader_tool, exercise_planning_tool], # Assuming exercise_planning_tool is complete
    allow_delegation=False
)