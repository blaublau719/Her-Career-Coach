from crewai import Agent, Task, Crew
from .models import JobApplicationRequest, JobApplicationResponse
from .config import Config
import json

class SimpleAnschreibenService:
    def __init__(self):
        Config.validate_config()
    
    def generate_application_materials(self, request: JobApplicationRequest) -> JobApplicationResponse:
        """Generate basic cover letter without complex tools"""
        
        try:
            # Create simple agents
            job_analyst = Agent(
                role="Job Analyst",
                goal="Extract key information from the job posting",
                backstory="You are an expert at analyzing job postings and extracting key information.",
                verbose=True
            )
            
            profile_creator = Agent(
                role="Profile Creator",
                goal="Create a professional profile based on resume content",
                backstory="You create comprehensive professional profiles from resume information.",
                verbose=True
            )
            
            letter_writer = Agent(
                role="Cover Letter Writer", 
                goal="Write a personalized cover letter",
                backstory="You write compelling cover letters that match candidates with job requirements.",
                verbose=True
            )
            
            # Create simple tasks
            job_task = Task(
                description=f"Analyze this job posting URL: {request.posting_url}. Extract and format the information as follows:\nJob Title: [title]\nCompany Name: [company]\nKey Requirements: [list main requirements]\nLocation: [location]\nSalary/Benefits: [if available]\nJob Type: [full-time/part-time/contract etc.]",
                expected_output="A structured summary with each field on a new line, formatted as 'Field Name: Value'",
                agent=job_analyst
            )
            
            profile_task = Task(
                description=f"Based on this resume content: {request.resume_content[:2000]}... Create a professional profile highlighting key skills, experience, and qualifications.",
                expected_output="A professional profile summary highlighting the candidate's key strengths.",
                agent=profile_creator
            )
            
            letter_task = Task(
                description=f"""Write a German cover letter (Anschreiben) for this candidate.
                
                Job Information: Use the job analysis from the Job Analyst.
                Candidate Profile: Use the profile from the Profile Creator.
                Candidate Motivation: {request.motivation}
                Personal Statement: {request.personal_statement}
                
                Create a professional, one-page cover letter in German that:
                1. Addresses the specific job and company
                2. Highlights relevant qualifications
                3. Shows genuine interest and motivation
                4. Uses a professional but personal tone
                """,
                expected_output="A complete German cover letter (Anschreiben) ready to send.",
                agent=letter_writer,
                context=[job_task, profile_task]
            )
            
            # Create crew
            crew = Crew(
                agents=[job_analyst, profile_creator, letter_writer],
                tasks=[job_task, profile_task, letter_task],
                verbose=True
            )
            
            # Execute
            result = crew.kickoff()
            
            # Parse results - extract string content from TaskOutput objects
            job_result = str(job_task.output.raw) if hasattr(job_task, 'output') and job_task.output else "Job analysis completed"
            profile_result = str(profile_task.output.raw) if hasattr(profile_task, 'output') and profile_task.output else "Profile created"
            cover_letter_result = str(letter_task.output.raw) if hasattr(letter_task, 'output') and letter_task.output else str(result)
            
            # Parse job result into structured format if possible
            try:
                # Try to parse the job analysis into structured data
                job_lines = job_result.strip().split('\n')
                job_data = {}
                for line in job_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        job_data[key.strip()] = value.strip()
                
                # If we got structured data, use it, otherwise use raw text
                if len(job_data) >= 3:  # At least 3 fields parsed
                    job_description = job_data
                else:
                    job_description = {"Raw Analysis": job_result}
            except:
                job_description = {"Raw Analysis": job_result}
            
            # Create response
            response_data = {
                "job_description": job_description,
                "client_profile": profile_result,
                "cover_letter": cover_letter_result
            }
            
            return JobApplicationResponse(**response_data)
            
        except Exception as e:
            print(f"Error in generation: {e}")
            # Return error response
            return JobApplicationResponse(
                job_description={"error": str(e)},
                client_profile="Error generating profile",
                cover_letter="Error generating cover letter"
            )