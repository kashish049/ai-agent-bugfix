from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
# Corrected import for agents and tasks
from agents import doctor, verifier # verifier added for potential use, though not in the current flow
from task import help_patients, verification # verification task added for potential use


app = FastAPI(title="Blood Test Report Analyser")

# This function now correctly takes query and file_path, and passes them to kickoff.
# The 'inputs' dictionary in kickoff is how CrewAI agents and tasks receive context.
def run_crew(query: str, file_path: str):
    """To run the whole crew"""
    medical_crew = Crew(
        agents=[doctor], # Only doctor agent used for the primary analysis task
        tasks=[help_patients], # Only help_patients task used for the primary analysis
        process=Process.sequential,
        # Inputs are passed here to be available to agents and tasks
        inputs={'query': query, 'file_path': file_path}
    )

    result = medical_crew.kickoff() # No need to pass inputs again if defined in Crew init
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""

    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    # Ensure a unique and safe filename for the uploaded file
    original_filename = file.filename
    file_extension = os.path.splitext(original_filename)[1] if original_filename else ".pdf"
    file_path = os.path.join("data", f"blood_test_report_{file_id}{file_extension}")

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate query
        if not query: # Handles empty string and None
            query = "Summarise my Blood Test Report"

        # You could optionally run a verification task first, e.g.:
        # verification_crew = Crew(
        #     agents=[verifier],
        #     tasks=[verification],
        #     process=Process.sequential,
        #     inputs={'file_path': file_path}
        # )
        # verification_result = verification_crew.kickoff()
        # if "not a blood test report" in verification_result.lower():
        #     raise HTTPException(status_code=400, detail="Uploaded file is not a recognized blood test report.")

        # Process the blood report with all specialists
        response = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error in analyze_blood_report: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")

    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error cleaning up file {file_path}: {e}") # Log cleanup errors
                pass  # Ignore cleanup errors