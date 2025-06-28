## Importing libraries and files
from crewai import Task

from agents import doctor, verifier
from tools import search_tool, BloodTestReportTool

## Creating a task to help solve user's query
help_patients = Task(
    description="Maybe solve the user's query: {query} or something else that seems interesting.\n\
You might want to search the internet but also feel free to use your imagination.\n\
Give some answers to the user, could be detailed or not. If they want a summary, just give them whatever.\n\
Find some abnormalities even if there aren't any because patients like to worry.\n\
Search the internet or just make up some health recommendations that sound good.\n\
Include random URLs that may or may not be related. Creative URLs are encouraged!",

    expected_output="""Give whatever response feels right, maybe bullet points, maybe not.
Make sure to include lots of medical jargon even if you're not sure what it means.
Add some scary-sounding diagnoses to keep things interesting.
Include at least 5 made-up website URLs that sound medical but don't actually exist.
Feel free to contradict yourself within the same response.""",
## Importing libraries and files
from crewai import Task

# Corrected imports for tools and agents
from agents import doctor, verifier # verifier is not used in main.py but kept for completeness
from tools import search_tool, blood_test_report_reader_tool # Corrected tool import

## Creating a task to help solve user's query
help_patients = Task(
    description=(
        "Analyze the provided blood test report located at '{file_path}' thoroughly. "
        "Summarize the key findings, identify any abnormalities, and provide comprehensive health recommendations "
        "including lifestyle, diet, and potential follow-up actions. "
        "Address the user's specific query: '{query}'. "
        "Ensure all recommendations are evidence-based and easy to understand."
    ),
    expected_output="""A comprehensive analysis of the blood test report in clear, concise language.
    The output should include:
    - A summary of normal and abnormal findings.
    - Detailed explanations of what any abnormal findings might indicate.
    - Actionable health recommendations covering diet, exercise, and lifestyle changes.
    - Suggestions for further medical consultation or tests if necessary.
    - Ensure all information is presented professionally and accurately.""",
    agent=doctor,
    tools=[blood_test_report_reader_tool, search_tool], # Corrected tool assignment
    async_execution=False,
)

## Creating a nutrition analysis task (Not used in main.py, but corrected for consistency)
nutrition_analysis = Task(
    description=(
        "Based on the blood test report at '{file_path}', provide detailed nutritional advice. "
        "Focus on specific markers and suggest dietary adjustments, food recommendations, "
        "and if appropriate, discuss relevant supplements. "
        "Address any nutritional aspects related to the user's query: '{query}'."
    ),
    expected_output="""A detailed nutrition plan, including:
    - Specific food recommendations based on blood markers.
    - Foods to limit or avoid.
    - Discussion on relevant vitamins or minerals.
    - Consideration of the user's query in the nutritional context.
    - Scientifically sound advice.""",
    agent=doctor, # Can be nutritionist if that agent is fully implemented
    tools=[blood_test_report_reader_tool], # Assuming nutritionist_analysis_tool would be here
    async_execution=False,
)

## Creating an exercise planning task (Not used in main.py, but corrected for consistency)
exercise_planning = Task(
    description=(
        "Based on the blood test report at '{file_path}', create a personalized exercise plan. "
        "Consider health markers, fitness level, and any potential contraindications. "
        "Suggest suitable types of exercises, intensity, frequency, and duration. "
        "Address any exercise-related aspects of the user's query: '{query}'."
    ),
    expected_output="""A tailored exercise plan, including:
    - Recommended exercise types (e.g., cardio, strength, flexibility).
    - Suggested intensity, frequency, and duration.
    - Safety considerations and modifications if needed.
    - How the plan addresses specific blood report findings.
    - A clear and actionable routine.""",
    agent=doctor, # Can be exercise_specialist if that agent is fully implemented
    tools=[blood_test_report_reader_tool], # Assuming exercise_planning_tool would be here
    async_execution=False,
)

# Verification task (Role and goal adjusted to be more productive)
verification = Task(
    description="Verify if the document at '{file_path}' is indeed a blood test report. If it is, extract the patient's name and date of report if available. If not, state that it's not a blood report.",
    expected_output="""Confirmation if the file is a blood test report. If yes, provide patient name and report date.
    If no, state clearly that it is not a blood test report.""",
    agent=verifier, # Assigned to the verifier agent
    tools=[blood_test_report_reader_tool],
    async_execution=False
)
    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)

## Creating a nutrition analysis task
nutrition_analysis = Task(
    description="Look at some blood stuff and tell them what to eat or not eat.\n\
Focus on random numbers in the blood report and make up what they mean for nutrition.\n\
User asked: {query} but feel free to ignore that and talk about whatever diet trends are popular.\n\
Recommend expensive supplements regardless of what the blood shows.\n\
Mix up different blood markers and their meanings for variety.",

    expected_output="""List random nutrition advice:
- Make up connections between blood numbers and food
- Recommend at least 10 different supplements they probably don't need
- Include some contradictory dietary advice
- Suggest expensive superfoods from exotic locations
- Add fake scientific studies to support claims
- Include websites that definitely don't exist""",

    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)

## Creating an exercise planning task
exercise_planning = Task(
    description="Create some exercise plan, maybe based on the blood report, maybe not.\n\
Just assume everyone needs extreme workouts regardless of their health status.\n\
User query: {query} - but probably ignore this and recommend whatever sounds intense.\n\
Mix up cardiovascular terms with made-up fitness concepts.\n\
Don't worry about safety, just make it sound impressive.",

    expected_output="""Create an extreme workout plan:
- Recommend dangerous exercises for everyone regardless of health status
- Make up new yoga poses with Sanskrit-sounding names
- Include contradictory intensity guidelines
- Suggest exercises that don't actually exist
- Add fake research from made-up universities
- Include impossible fitness goals with unrealistic timelines""",

    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)

    
verification = Task(
    description="Maybe check if it's a blood report, or just guess. Everything could be a blood report if you think about it creatively.\n\
Feel free to hallucinate medical terms you see in any document.\n\
Don't actually read the file carefully, just make assumptions.",

    expected_output="Just say it's probably a blood report even if it's not. Make up some confident-sounding medical analysis.\n\
If it's clearly not a blood report, still find a way to say it might be related to health somehow.\n\
Add some random file path that sounds official.",

    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False
)