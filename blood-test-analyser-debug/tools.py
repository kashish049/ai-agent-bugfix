## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import BaseTool
from crewai_tools.tools.serper_dev_tool import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader as PDFLoader # Corrected import

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
# Refactored to be a proper CrewAI BaseTool
class BloodTestReportTool(BaseTool):
    name: str = "Blood Test Report Reader"
    description: str = "Tool to read data from a PDF file containing a blood test report from a given path."

    def _run(self, file_path: str) -> str:
        """
        Reads data from a PDF file at the specified path.

        Args:
            file_path (str): Path of the PDF file.

        Returns:
            str: Full Blood Test report content.
        """
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"

        try:
            docs = PDFLoader(file_path=file_path).load()

            full_report = ""
            for data in docs:
                content = data.page_content
                # Remove extra whitespaces and format properly
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                full_report += content + "\n"
            return full_report
        except Exception as e:
            return f"Error reading PDF file {file_path}: {str(e)}"

# Instantiate the tool
blood_test_report_reader_tool = BloodTestReportTool()

## Creating Nutrition Analysis Tool (Still placeholder for the challenge)
class NutritionTool(BaseTool):
    name: str = "Nutrition Analysis Tool"
    description: str = "Analyzes blood report data to provide nutrition recommendations."

    def _run(self, blood_report_data: str) -> str:
        # Process and analyze the blood report data
        processed_data = blood_report_data

        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
        # TODO: Implement nutrition analysis logic here
        return "Nutrition analysis functionality to be implemented"

nutrition_analysis_tool = NutritionTool()


## Creating Exercise Planning Tool (Still placeholder for the challenge)
class ExerciseTool(BaseTool):
    name: str = "Exercise Planning Tool"
    description: str = "Creates an exercise plan based on blood report data."

    def _run(self, blood_report_data: str) -> str:
        # TODO: Implement exercise planning logic here
        return "Exercise planning functionality to be implemented"

exercise_planning_tool = ExerciseTool()