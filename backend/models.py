from pydantic import BaseModel, Field
from typing import Optional

class JobDescription(BaseModel):
    Job_Title: str = Field(..., description="EXTRACT ONLY: The exact job title as mentioned in the posting. If not found, use 'Information not available'")
    Company_Name: str = Field(..., description="EXTRACT ONLY: The actual company name from the posting content. If not found, use 'Information not available'. NEVER use examples like 'Tech Solutions Inc.'")
    Job_Description: str = Field(..., description="EXTRACT ONLY: A summary of what the job role entails based on the posting content. If not found, use 'Information not available'")
    Key_Responsibilities: str = Field(..., description="EXTRACT ONLY: Specific duties mentioned in the posting. If not found, use 'Information not available'")
    Qualifications_and_Requirements: str = Field(..., description="EXTRACT ONLY: Requirements mentioned in the posting. If not found, use 'Information not available'")
    Location: str = Field(..., description="EXTRACT ONLY: Work location mentioned in the posting. If not found, use 'Information not available'")
    Benefits_Salary: str = Field(..., description="EXTRACT ONLY: Compensation/benefits mentioned in the posting. If not found, use 'Information not available'")
    Company_Overview: str = Field(..., description="EXTRACT ONLY: Company information from the posting. If not found, use 'Information not available'")

class CompInfo(BaseModel):
    serper_result: str = Field(..., description="Raw search results from Serper API for the company")
    company_name: str = Field(..., description="The official company name")
    company_core_business: str = Field(..., description="Main business activities, products, or services the company provides")
    company_location: str = Field(..., description="Company headquarters or main office locations")
    company_kununu_score: str = Field(..., description="Kununu rating/score if available, or 'Not found' if unavailable")
    employee_reviews: str = Field(..., description="Summary of employee reviews and overall reputation")
    number_employee: str = Field(..., description="Company size in terms of number of employees")

class JobApplicationRequest(BaseModel):
    posting_url: str = Field(..., description="URL of the job posting to analyze")
    resume_content: str = Field(..., description="The client's resume content as text")
    motivation: str = Field(..., description="Client's motivation and interest for applying to this specific job")
    personal_statement: Optional[str] = Field("", description="Optional personal statement or additional information about the client")
    
class JobApplicationResponse(BaseModel):
    job_description: dict = Field(..., description="Structured analysis of the job posting containing title, company, requirements, etc.")
    client_profile: str = Field(..., description="Comprehensive profile of the client based on their resume and personal statement")
    cover_letter: str = Field(..., description="Generated German cover letter (Anschreiben) tailored for the job")
    company_profile: Optional[dict] = Field(None, description="Research results about the company including background, culture, and reviews")
    refined_resume: Optional[str] = Field(None, description="Optimized version of the client's resume tailored for the specific job")