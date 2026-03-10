from crewai import Crew
from .agents import AnschreibenAgents
from .tasks import AnschreibenTasks
from .models import JobApplicationRequest, JobApplicationResponse
from .config import Config
import json
import os
import uuid
import shutil
import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import RequestException

class AnschreibenService:
    def __init__(self):
        Config.validate_config()
        self.agents = AnschreibenAgents()
        self.tasks = AnschreibenTasks()
    
    def _extract_url_content(self, url: str) -> str:
        """Extract text content from URL using direct web scraping"""
        def exponential_backoff_delay(attempt):
            return min(60, 5 * (2 ** attempt))  # Sleep delay: 5, 10, 20 seconds

        for attempt in range(3):
            try:
                timeout = 30  # Fixed 30 second timeout for all attempts
                
                # Add headers to mimic a real browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                
                response = requests.get(url, timeout=timeout, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                
                # Get text and clean it up
                text = soup.get_text()
                
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                
                print(f"[DEBUG] Successfully extracted {len(text)} characters from URL")
                print(f"[DEBUG] First 500 characters: {text[:500]}")
                
                return text
            except RequestException as e:
                if attempt == 2:  # Last attempt
                    return f"Error scraping the website after 3 attempts: {str(e)}"
                delay = exponential_backoff_delay(attempt)
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
        
        return "Failed to scrape the website"
        
    def generate_application_materials(self, request: JobApplicationRequest) -> JobApplicationResponse:
        """Generate complete application materials including cover letter and analysis"""
        
        # Create unique session directory for outputs
        session_id = str(uuid.uuid4())
        output_dir = f"outputs/{session_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract URL content directly
        job_posting_content = self._extract_url_content(request.posting_url)
        
        # Log extracted content for debugging
        print(f"[DEBUG] Extracted content length: {len(job_posting_content)}")
        print(f"[DEBUG] Content preview: {job_posting_content[:200]}...")
        
        # Validate content extraction
        if job_posting_content.startswith("Error scraping") or job_posting_content == "Failed to scrape the website" or len(job_posting_content.strip()) < 100:
            print("[DEBUG] Content extraction failed - setting error message")
            job_posting_content = f"Unable to extract content from URL: {request.posting_url}\n\nPlease provide the job posting content manually or check if the URL is accessible."
        
        # Create agents (no tools needed for post_extractor since content is pre-extracted)
        post_extractor = self.agents.create_post_extractor()
        client_knower = self.agents.create_client_knower()
        cover_letter_writer = self.agents.create_cover_letter_writer()
        fact_checker = self.agents.create_fact_checker()
        
        # Create tasks without web scraping tools
        job_task = self.tasks.create_job_analysis_task(post_extractor, None)
        client_task = self.tasks.create_client_profile_task(client_knower)
        cover_letter_task = self.tasks.create_cover_letter_task(cover_letter_writer, client_task, job_task)
        fact_check_task = self.tasks.create_fact_check_task(fact_checker, client_task, job_task, cover_letter_task)
        
        # Create crew with simpler configuration
        crew = Crew(
            agents=[post_extractor, client_knower, cover_letter_writer],
            tasks=[job_task, client_task, cover_letter_task],
            verbose=True,
            max_execution_time=300  # 5 minute timeout
        )
        
        # Prepare inputs with extracted content
        inputs = {
            "PostingURL": request.posting_url,
            "job_posting_content": job_posting_content,
            "resumeContent": request.resume_content,
            "Motivation": request.motivation,
            "Personal_Statement": request.personal_statement,
            "comp_name": "default"
        }
        
        # Execute crew
        result = crew.kickoff(inputs=inputs)
        
        print(f"[DEBUG] Crew result type: {type(result)}")
        print(f"[DEBUG] Crew result: {result}")
        
        # Initialize response data
        response_data = {
            "job_description": {},
            "client_profile": "",
            "cover_letter": ""
        }
        
        # Try to extract job description from crew result - using raw text parsing
        try:
            # Get the raw text output from the first task
            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
                job_task_result = result.tasks_output[0]  # First task is job analysis
                raw_output = str(job_task_result.raw)
                print(f"[DEBUG] Raw task output: {raw_output}")
                
                # Try to parse JSON from the raw output
                import re
                json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    print(f"[DEBUG] Extracted JSON string: {json_str}")
                    try:
                        job_desc = json.loads(json_str)
                        print(f"[DEBUG] Successfully parsed JSON: {job_desc}")
                    except json.JSONDecodeError as e:
                        print(f"[ERROR] Failed to parse JSON: {e}")
                        job_desc = {"error": f"Invalid JSON in response: {json_str[:200]}..."}
                else:
                    print(f"[ERROR] No JSON found in raw output")
                    job_desc = {"error": f"No JSON found in agent response: {raw_output[:200]}..."}
            else:
                print(f"[DEBUG] Result structure: {dir(result)}")
                if hasattr(result, 'raw'):
                    raw_output = str(result.raw)
                    print(f"[DEBUG] Direct raw output: {raw_output}")
                    job_desc = {"error": f"Direct raw output: {raw_output[:200]}..."}
                else:
                    job_desc = {"error": "No task outputs or raw output found"}
                
            response_data["job_description"] = job_desc
                
        except Exception as e:
            print(f"[ERROR] Failed to extract job description from result: {str(e)}")
            response_data["job_description"] = {"error": f"Error extracting job description: {str(e)}"}
        
        # Try to read client profile
        try:
            with open("client_profile.md", "r", encoding="utf-8") as f:
                response_data["client_profile"] = f.read()
        except FileNotFoundError:
            response_data["client_profile"] = "Client profile not generated"
        
        # Try to read final cover letter (fact-checked version)
        try:
            with open("cover_letter_checked.md", "r", encoding="utf-8") as f:
                response_data["cover_letter"] = f.read()
        except FileNotFoundError:
            # Fallback to unchecked version
            try:
                with open("cover_letter.md", "r", encoding="utf-8") as f:
                    response_data["cover_letter"] = f.read()
            except FileNotFoundError:
                response_data["cover_letter"] = "Cover letter not generated"
        
        # Move files to session directory
        for filename in ["job_description.json", "client_profile.md", "cover_letter.md", "cover_letter_checked.md"]:
            if os.path.exists(filename):
                shutil.move(filename, os.path.join(output_dir, filename))
        
        return JobApplicationResponse(**response_data)
    
    def generate_with_company_research(self, request: JobApplicationRequest) -> JobApplicationResponse:
        """Generate application materials with company research"""
        
        # Create unique session directory for outputs
        session_id = str(uuid.uuid4())
        output_dir = f"outputs/{session_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract URL content directly
        job_posting_content = self._extract_url_content(request.posting_url)
        
        # Create agents
        post_extractor = self.agents.create_post_extractor()
        client_knower = self.agents.create_client_knower()
        company_investigator = self.agents.create_company_investigator()
        resume_improver = self.agents.create_resume_improver()
        cover_letter_writer = self.agents.create_cover_letter_writer()
        fact_checker = self.agents.create_fact_checker()
        
        # Create tasks (post_extractor doesn't need web scraper tool anymore)
        job_task = self.tasks.create_job_analysis_task(post_extractor, None)
        client_task = self.tasks.create_client_profile_task(client_knower)
        company_task = self.tasks.create_company_research_task(company_investigator, job_task)
        resume_task = self.tasks.create_resume_refinement_task(resume_improver, client_task, job_task)
        cover_letter_task = self.tasks.create_cover_letter_task(cover_letter_writer, client_task, job_task)
        fact_check_task = self.tasks.create_fact_check_task(fact_checker, client_task, job_task, cover_letter_task)
        
        # Create crew
        crew = Crew(
            agents=[post_extractor, client_knower, company_investigator, resume_improver, cover_letter_writer, fact_checker],
            tasks=[job_task, client_task, company_task, resume_task, cover_letter_task, fact_check_task],
            verbose=True,
            memory=True,
            planning=True
        )
        
        # Prepare inputs with extracted content
        inputs = {
            "PostingURL": request.posting_url,
            "job_posting_content": job_posting_content,
            "resumeContent": request.resume_content,
            "Motivation": request.motivation,
            "Personal_Statement": request.personal_statement,
            "comp_name": "default"
        }
        
        # Execute crew
        result = crew.kickoff(inputs=inputs)
        
        # Read generated files
        response_data = {
            "job_description": {},
            "client_profile": "",
            "cover_letter": "",
            "company_profile": {},
            "refined_resume": ""
        }
        
        # Read all generated files
        files_to_read = {
            "job_description": ("job_description.json", "json"),
            "client_profile": ("client_profile.md", "text"),
            "cover_letter": ("cover_letter_checked.md", "text"),
            "company_profile": ("company_profile.json", "json"),
            "refined_resume": ("refined_resume.md", "text")
        }
        
        for key, (filename, file_type) in files_to_read.items():
            try:
                if file_type == "json":
                    with open(filename, "r", encoding="utf-8") as f:
                        response_data[key] = json.load(f)
                else:
                    with open(filename, "r", encoding="utf-8") as f:
                        response_data[key] = f.read()
            except FileNotFoundError:
                if key == "cover_letter":
                    # Try fallback to unchecked version
                    try:
                        with open("cover_letter.md", "r", encoding="utf-8") as f:
                            response_data[key] = f.read()
                    except FileNotFoundError:
                        response_data[key] = "Cover letter not generated"
                else:
                    response_data[key] = f"{key.replace('_', ' ').title()} not generated"
        
        # Move files to session directory
        for filename in files_to_read.values():
            if os.path.exists(filename[0]):
                shutil.move(filename[0], os.path.join(output_dir, filename[0]))
        
        # Also move unchecked cover letter if it exists
        if os.path.exists("cover_letter.md"):
            shutil.move("cover_letter.md", os.path.join(output_dir, "cover_letter.md"))
        
        return JobApplicationResponse(**response_data)