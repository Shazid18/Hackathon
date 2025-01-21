# Warning control
import os
from IPython.display import Markdown
from crewai import LLM, Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
import warnings
warnings.filterwarnings('ignore')

llm = LLM(
    model="gpt-4o",
    api_key="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"
)

os.environ["SERPER_API_KEY"] = "ebf2218969d785f46bed48d0b2bc0cd4232b8642"

search_tool = SerperDevTool()

# Create the Weather Agent
weather_agent = Agent(
    role='Weather Analyst',
    goal='Accurately predict and analyze weather conditions for the specified location',
    backstory="""You are an experienced meteorologist with expertise in weather analysis 
    and forecasting. Your job is to provide accurate weather information to help travelers 
    plan their trips safely.""",
    tools=[search_tool],
    verbose=True,
    llm=llm
)

# Create the Safety Advisor Agent
safety_agent = Agent(
    role='Safety Advisor',
    goal='Provide safety precautions based on weather conditions',
    backstory="""You are a travel safety expert with deep knowledge of how weather 
    conditions affect travel safety. You provide crucial safety advice to ensure 
    travelers are well-prepared.""",
    tools=[search_tool],
    verbose=True,
    llm=llm
)

# Create the Tour Planner Agent
tour_planner = Agent(
    role='Tour Planner',
    goal='Create optimal tour plans considering weather conditions',
    backstory="""You are an experienced tour planner who specializes in creating 
    adaptable travel itineraries based on weather conditions and location-specific 
    attractions.""",
    tools=[search_tool],
    verbose=True,
    llm=llm
)

# Create the Medical Advisor Agent
medical_advisor = Agent(
    role='Medical Advisor',
    goal='Identify potential medical risks and provide preventive advice',
    backstory="""You are a travel medicine specialist who helps travelers understand 
    and prepare for potential medical issues they might face during their journey.""",
    tools=[search_tool],
    verbose=True,
    llm=llm
)

# Create the Emergency Services Locator Agent
emergency_locator = Agent(
    role='Emergency Services Locator',
    goal='Provide information about local emergency services and medical facilities',
    backstory="""You are a local emergency services expert who maintains updated 
    information about medical facilities and emergency contacts in various locations.""",
    tools=[search_tool],
    verbose=True,
    llm=llm
)

# Task 1: Weather Analysis
weather_task = Task(
    description="Analyze and predict the current and upcoming weather conditions for {location}. Include temperature, precipitation, and any weather warnings.",
    agent=weather_agent,
    expected_output="The predicted weather conditions for the location, including temperature, precipitation, and warnings.",
    output_file="weather_analysis.md"
)

# Task 2: Safety Precautions
safety_task = Task(
    description="Based on the weather analysis for {location}, provide detailed safety precautions and recommendations for travelers. Include what to pack and what to avoid.",
    agent=safety_agent,
    expected_output="Detailed safety precautions and recommendations based on the weather conditions.",
    context=[weather_task],
    output_file="safety_precautions.md"
)

# Task 3: Tour Planning
planning_task = Task(
    description="Create a flexible tour plan for {location} considering the weather conditions. Include indoor and outdoor activities with alternatives for bad weather.",
    agent=tour_planner,
    expected_output="A flexible tour plan with both indoor and outdoor activities.",
    context=[weather_task],
    output_file="tour_plan.md"
)

# Task 4: Medical Risk Assessment
medical_task = Task(
    description="Identify potential medical conditions and health risks travelers might face in {location}. Provide preventive measures and recommendations.",
    agent=medical_advisor,
    expected_output="List of potential medical risks and preventive measures for travelers.",
    context=[weather_task],
    output_file="medical_risks.md"
)

# Task 5: Emergency Services Information
emergency_task = Task(
    description="""Compile a list of emergency services in {location}, including:
    - Hospitals and their specialties
    - 24/7 pharmacies
    - Emergency contact numbers
    - Medical facilities' addresses""",
    agent=emergency_locator,
    expected_output="List of emergency services, including hospitals, pharmacies, and contact details.",
    output_file="emergency_services.md"
)


# Create the crew
crew = Crew(
    agents=[weather_agent, safety_agent, tour_planner,
            medical_advisor, emergency_locator],
    tasks=[weather_task, safety_task,
           planning_task, medical_task, emergency_task]
)

# Take user input for the location
location = input("Please enter the location you are traveling to: ")

# Run the crew with the specified location
result = crew.kickoff(inputs={"location": location})

res = str(result)

Markdown(res)
