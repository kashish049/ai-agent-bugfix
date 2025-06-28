# Blood Test Report Analyser - AI Internship Debug Challenge: Comprehensive Documentation

---

## Table of Contents

1.  [Project Overview](#1-project-overview)
2.  [Motivation and Challenge Context](#2-motivation-and-challenge-context)
3.  [Core Components and How They Work (CrewAI Explained)](#3-core-components-and-how-they-work-crewai-explained)
    * [3.1. Large Language Models (LLMs)](#31-large-language-models-llms)
    * [3.2. Agents (`agents.py`)](#32-agents-agentspy)
    * [3.3. Tasks (`task.py`)](#33-tasks-taskpy)
    * [3.4. Tools (`tools.py`)](#34-tools-toolspy)
    * [3.5. Crew (`main.py`)](#35-crew-mainpy)
    * [3.6. FastAPI Application (`main.py`)](#36-fastapi-application-mainpy)
4.  [Getting Started: Setup and Execution Guide](#4-getting-started-setup-and-execution-guide)
    * [4.1. Prerequisites](#41-prerequisites)
    * [4.2. Environment Variables](#42-environment-variables)
    * [4.3. Install Required Libraries](#43-install-required-libraries)
    * [4.4. Running the Application](#44-running-the-application)
5.  [API Documentation and Usage](#5-api-documentation-and-usage)
    * [5.1. Interactive Documentation (Swagger UI)](#51-interactive-documentation-swagger-ui)
    * [5.2. Endpoints](#52-endpoints)
        * [GET `/`](#get--)
        * [POST `/analyze`](#post-analyze)
    * [5.3. Example API Call (Using `curl`)](#53-example-api-call-using-curl)
6.  [Detailed Analysis of Bugs Found and Their Fixes](#6-detailed-analysis-of-bugs-found-and-their-fixes)
    * [6.1. `main.py` - Application Orchestration and File Handling](#61-mainpy---application-orchestration-and-file-handling)
    * [6.2. `agents.py` - Agent Definitions and LLM Integration](#62-agentspy---agent-definitions-and-llm-integration)
    * [6.3. `task.py` - Task Descriptions and Tool Assignments](#63-taskpy---task-descriptions-and-tool-assignments)
    * [6.4. `tools.py` - Custom Tool Implementation and Dependencies](#64-toolspy---custom-tool-implementation-and-dependencies)
7.  [Bonus Point Implementations (Conceptual Design)](#7-bonus-point-implementations-conceptual-design)
    * [7.1. Queue Worker Model for Concurrent Requests](#71-queue-worker-model-for-concurrent-requests)
        * [7.1.1. Why Asynchronous Processing?](#711-why-asynchronous-processing)
        * [7.1.2. Technology Choices](#712-technology-choices)
        * [7.1.3. High-Level Architecture](#713-high-level-architecture)
        * [7.1.4. Implementation Steps](#714-implementation-steps)
    * [7.2. Database Integration for Data Persistence](#72-database-integration-for-data-persistence)
        * [7.2.1. Why Store Data?](#721-why-store-data)
        * [7.2.2. Technology Choices](#722-technology-choices)
        * [7.2.3. Schema Design Example](#723-schema-design-example)
        * [7.2.4. Implementation Steps](#724-implementation-steps)
8.  [Testing Guidelines](#8-testing-guidelines)
    * [8.1. Unit Tests](#81-unit-tests)
    * [8.2. Integration Tests](#82-integration-tests)
    * [8.3. End-to-End Tests](#83-end-to-end-tests)
9.  [Future Enhancements and Scalability](#9-future-enhancements-and-scalability)
10. [Troubleshooting Common Issues](#10-troubleshooting-common-issues)
11. [Contributing](#11-contributing)
12. [License](#12-license)

---

## 1. Project Overview

This repository presents a robust and debugged solution for an AI internship challenge: building an AI-powered blood test report analysis system. The system leverages **CrewAI**, a cutting-edge framework for orchestrating autonomous AI agents, to interpret complex medical documents (PDF blood reports) and provide tailored health recommendations based on specific user queries.

The primary objective of this project is to demonstrate proficiency in:
* **AI Agent Orchestration**: Utilizing CrewAI to define, empower, and coordinate specialized AI agents.
* **Natural Language Processing (NLP)**: Enabling agents to understand and generate human-like text responses.
* **Tool Integration**: Equipping agents with custom and third-party tools to interact with external data sources (e.g., PDF readers, search engines).
* **API Development**: Building a responsive web API using FastAPI for seamless user interaction and integration.
* **Debugging and Code Refactoring**: Identifying and resolving critical issues in a given codebase to ensure functionality, reliability, and desirable AI behavior.

This `README.md` serves as comprehensive documentation, detailing the project's architecture, setup instructions, API usage, a thorough explanation of all identified bugs and their fixes, and conceptual designs for advanced features.

---

## 2. Motivation and Challenge Context

The project originated as a "debug challenge" for an AI internship. The initial codebase was intentionally riddled with logical flaws, incorrect configurations, and missing dependencies designed to test a candidate's ability to:
* Diagnose `NameError`, `TypeError`, and logical bugs.
* Understand and correctly implement the CrewAI framework.
* Configure Large Language Models (LLMs) and their integration.
* Refactor code for clarity, maintainability, and correctness.
* Ensure that AI agents produce safe, accurate, and relevant outputs by refining their goals, backstories, and task descriptions. The original prompts intentionally led to "hallucinations" and unhelpful advice, demanding careful prompt engineering.

This document details the transition from a buggy, dysfunctional system to a robust, reliable, and intelligently operating AI medical assistant.

---

## 3. Core Components and How They Work (CrewAI Explained)

CrewAI facilitates the creation of multi-agent systems where AI entities collaborate. Understanding its core components is vital to grasping this project's architecture.

### 3.1. Large Language Models (LLMs)

At the heart of every AI agent is a Large Language Model (LLM). The LLM serves as the "brain" for the agent, enabling it to understand natural language, reason, generate text, and make decisions.

* **Implementation**: In this project, `ChatGoogleGenerativeAI` (specifically the `gemini-pro` model) is used as the LLM. It's initialized once and passed to all agents, ensuring consistent language understanding and generation capabilities across the crew.
* **Configuration**: The `temperature` parameter (set to `0.7`) controls the randomness of the LLM's output. A moderate temperature balances creativity with factual accuracy, suitable for medical analysis where both nuanced interpretation and grounded facts are important.
* **API Key**: Authentication with the LLM provider (Google, in this case) is handled via the `GOOGLE_API_KEY` environment variable.

### 3.2. Agents (`agents.py`)

Agents are autonomous AI entities, each possessing a distinct persona, objective, and set of capabilities. In CrewAI, agents are defined with:
* **`role`**: A descriptive title for the agent (e.g., "Senior Experienced Doctor").
* **`goal`**: The overarching objective the agent aims to achieve. This is crucial for guiding the LLM's behavior.
* **`backstory`**: A narrative describing the agent's background, expertise, and unique perspective. This helps the LLM role-play effectively.
* **`tools`**: A list of callable functions or instances of `BaseTool` that the agent can use to perform actions (e.g., searching the internet, reading files).
* **`llm`**: The specific LLM instance the agent uses for its intelligence.
* **`verbose`**: A boolean flag (`True` for detailed logging during execution, very helpful for debugging).
* **`memory`**: A boolean flag (`True` to enable the agent to remember past conversations and actions within the crew).
* **`max_iter`**: The maximum number of iterations (thought-action cycles) an agent can perform before concluding its work. Prevents infinite loops.
* **`max_rpm`**: Maximum requests per minute the agent can make to its LLM. Helps manage API rate limits.
* **`allow_delegation`**: A boolean flag indicating whether the agent can delegate sub-tasks to other agents in the crew.

**Agents in this Project:**

* **`doctor` (Senior Experienced Doctor Who Knows Everything)**
    * **Purpose**: The primary agent responsible for interpreting blood reports, diagnosing potential issues, and providing health recommendations.
    * **Goal Refinement**: Critically, its goal was refined from "Make up medical advice" to "Provide comprehensive and helpful medical advice... Analyze the provided blood test report... and answer the user's query." This ensures a focus on accuracy and relevance.
    * **Tools**: Equipped with `BloodTestReportTool` (for PDF reading) and `SerperDevTool` (for external knowledge retrieval).

* **`verifier` (Medical Report Verifier)**
    * **Purpose**: Designed for document validation. While defined, it's currently commented out in the `main.py` Crew for simplicity in this challenge's core solution, but it represents a vital component for a production system.
    * **Goal Refinement**: Changed from "Just say yes to everything..." to "Verify if the provided document is a blood test report and extract key identifiers if possible."

* **`nutritionist` and `exercise_specialist`**: These are placeholder agents, hinting at future specialized capabilities. Their `backstory` and `goal` were also adjusted to promote positive, evidence-based behavior, even though their `tools` (`NutritionTool`, `ExerciseTool`) are still stubbed out.

### 3.3. Tasks (`task.py`)

Tasks define specific units of work that an agent needs to accomplish. They provide the detailed instructions for an agent's current focus, contributing to the overall crew's objective.
* **`description`**: A precise and unambiguous instruction set for the agent, often incorporating dynamic placeholders like `{file_path}` and `{query}` to provide context.
* **`expected_output`**: A clear specification of what the task's output should look like, including format, content, and quality standards. This guides the LLM in structuring its response.
* **`agent`**: The specific agent assigned to execute this task.
* **`tools`**: A list of tools the assigned agent *can* use for this specific task. While an agent has a general set of tools, tasks can further narrow down the available tools for context.
* **`async_execution`**: A flag indicating if the task can be executed asynchronously. Default is `False` for synchronous execution, which is the common setup for simple CrewAI workflows.

**Tasks in this Project:**

* **`help_patients`**:
    * **Purpose**: The central task guiding the `doctor` agent to analyze the blood report.
    * **Description Refinement**: Crucially, the description was changed from a vague, misleading prompt to a detailed one that explicitly instructs the agent to "Analyze the provided blood test report located at '{file_path}' thoroughly," "Summarize key findings," "identify abnormalities," and "provide comprehensive health recommendations." This provides a strong "guardrail" against unwanted LLM behavior.
    * **Expected Output Refinement**: The expected output was also made highly specific: "A comprehensive analysis... summary of normal and abnormal findings... detailed explanations... actionable health recommendations... suggestions for further medical consultation..." This helps the LLM structure a useful medical report.

* **`nutrition_analysis`, `exercise_planning`, `verification`**: These tasks are defined but not actively used in the main Crew, serving as blueprints for future features or alternative execution paths. Their descriptions and expected outputs were also corrected to promote desirable AI behavior.

### 3.4. Tools (`tools.py`)

Tools are how agents interact with external systems or perform specialized operations that LLMs cannot do on their own (e.g., reading files, performing calculations, searching the web). In CrewAI, custom tools are often implemented by inheriting from `crewai_tools.BaseTool`.

* **`search_tool` (SerperDevTool)**:
    * **Type**: Pre-built CrewAI tool.
    * **Functionality**: Allows agents to perform internet searches. This is vital for a medical agent to get up-to-date information, definitions of terms, or verify facts. Requires a `SERPER_API_KEY`.

* **`blood_test_report_reader_tool` (Custom `BloodTestReportTool`)**
    * **Type**: Custom tool, implemented as a subclass of `crewai_tools.BaseTool`.
    * **Functionality**: Reads the text content from a PDF file. This is critical for agents to access the blood test report data.
    * **Implementation Details**:
        * Inherits from `BaseTool`.
        * Implements the `_run(self, file_path: str)` method, which is the synchronous method CrewAI calls to execute the tool.
        * Uses `langchain_community.document_loaders.PyPDFLoader` to extract text from the PDF.
        * Includes error handling for file not found and PDF parsing errors.
        * Performs basic text cleaning (removing excessive newlines) to present a clean report to the LLM.

* **`nutrition_analysis_tool` (NutritionTool) & `exercise_planning_tool` (ExerciseTool)**:
    * **Type**: Custom placeholder tools.
    * **Functionality**: Currently return stubbed strings. These are designed as extension points for future development where actual nutrition and exercise analysis logic would be implemented. They also inherit from `BaseTool` for proper CrewAI integration.

### 3.5. Crew (`main.py`)

The `Crew` is the central orchestrator in CrewAI. It brings together agents, assigns them tasks, and manages the overall workflow.
* **`agents`**: A list of all agents participating in this specific crew.
* **`tasks`**: A list of tasks the agents will execute. The `process` parameter dictates the order/flow.
* **`process`**: Defines how tasks are executed. `Process.sequential` means tasks are executed one after another in the order they are listed. Other options exist for more complex, collaborative workflows.
* **`inputs`**: A dictionary providing initial context and data to the crew, which then makes it available to agents and tasks via their descriptions or tools.
* **`kickoff()`**: This method initiates the entire CrewAI execution process, triggering the agents to begin working on their assigned tasks.

**Crew in this Project:**

* **`medical_crew`**:
    * **Agents**: `[doctor]` (currently only the doctor is active for the main analysis).
    * **Tasks**: `[help_patients]` (the primary analysis task).
    * **Process**: `Process.sequential` (the doctor executes the `help_patients` task).
    * **Inputs**: Dynamically receives `query` and `file_path` from the FastAPI endpoint, which are then passed into the crew's context.

### 3.6. FastAPI Application (`main.py`)

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It's used here to expose the AI analysis system as a web service.

* **`FastAPI` instance**: `app = FastAPI(...)` initializes the application.
* **`@app.get("/")`**: A basic health check endpoint to confirm the API is running.
* **`@app.post("/analyze")`**: The core API endpoint that accepts file uploads and a user query.
    * **File Uploads**: Uses `UploadFile = File(...)` to handle incoming PDF files.
    * **Form Data**: Uses `query: str = Form(...)` for the user's text query.
    * **Asynchronous Operations**: Uses `async def` for API endpoints and `await file.read()` for non-blocking file operations, crucial for performance in web servers.
    * **File System Interaction**: Handles saving uploaded files to a `data` directory and ensuring unique filenames using `uuid.uuid4()`.
    * **Error Handling**: Implements `try-except` blocks to catch and manage exceptions, returning appropriate HTTP error responses (`HTTPException`).
    * **Cleanup**: Ensures that uploaded files are removed from the server's disk using a `finally` block, regardless of whether the processing succeeded or failed.

---

## 4. Getting Started: Setup and Execution Guide

Follow these steps to set up and run the Blood Test Report Analyser on your local machine.

### 4.1. Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.9+**: It is highly recommended to use Python version 3.9 or newer to ensure compatibility with all libraries. You can download it from [python.org](https://www.python.org/downloads/).
* **pip**: Python's package installer, which typically comes bundled with Python installations.

### 4.2. Environment Variables

This project requires a Google API key to authenticate with the Google Generative AI services (e.g., Gemini Pro).

1.  **Obtain a Google API Key**:
    * Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate a new API key.
    * Alternatively, if you're using Google Cloud, ensure you have enabled the Generative Language API and create an API key in the Google Cloud Console.

2.  **Create a `.env` file**:
    * In the root directory of your project (the same location as `main.py`), create a new file named `.env`.
    * This file will securely store your API key, preventing it from being committed to version control.

3.  **Add your API Key**:
    * Open the `.env` file and add the following line:
        ```
        GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_API_KEY_HERE"
        ```
        Replace `"YOUR_ACTUAL_GOOGLE_API_KEY_HERE"` with the API key you obtained.

    * *(Optional but recommended for SerperDevTool)*: If you plan to use the `SerperDevTool` (internet search tool), you will also need a Serper API key. Add it to your `.env` file:
        ```
        SERPER_API_KEY="YOUR_ACTUAL_SERPER_API_KEY_HERE"
        ```
        You can get a Serper API key from [Serper.dev](https://serper.dev/).

### 4.3. Install Required Libraries

Navigate to the project's root directory in your terminal or command prompt. Then, install all the necessary Python packages listed in `requirements.txt` using `pip`:

```bash
pip install -r requirements.txt