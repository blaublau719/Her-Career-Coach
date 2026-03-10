#!/usr/bin/env python3
"""
Simple test script for CrewAI functionality
"""

from crewai import Agent, Task, Crew
from .config import Config

def test_simple_crew():
    """Test a minimal CrewAI setup"""
    Config.validate_config()
    
    # Create a simple agent
    analyst = Agent(
        role="Job Analyst",
        goal="Extract key information from the job posting URL: {job_url}",
        backstory="You are an expert at analyzing job postings and extracting key information.",
        verbose=True
    )
    
    # Create a simple task
    analysis_task = Task(
        description="Analyze the job posting at {job_url} and extract the job title, company name, and key requirements.",
        expected_output="A summary with job title, company name, and 3-5 key requirements.",
        agent=analyst
    )
    
    # Create crew
    crew = Crew(
        agents=[analyst],
        tasks=[analysis_task],
        verbose=True
    )
    
    # Test with a job URL
    result = crew.kickoff(inputs={
        "job_url": "https://jobs.dfki.de/ausschreibung/researcher-spatiotemporal-modelling-and-event-data-analysis-567802.html"
    })
    
    print("=" * 50)
    print("RESULT:")
    print("=" * 50)
    print(result)
    print("=" * 50)
    
    return result

if __name__ == "__main__":
    try:
        test_simple_crew()
        print("✅ Simple crew test successful!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()