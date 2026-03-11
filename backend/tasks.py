from crewai import Task
from .models import JobDescription, CompInfo


class AnschreibenTasks:
    @staticmethod
    def create_job_analysis_task(agent, web_scraper_tool):
        return Task(
            description=(
                "Your task is to extract job information and return ONLY a JSON object. No explanations, no additional text.\n\n"
                "JOB POSTING CONTENT:\n"
                "{job_posting_content}\n\n"
                "Return ONLY this JSON format (replace values with extracted information or 'Information not available'):\n"
                "{{\n"
                '  "Job_Title": "extract job title here",\n'
                '  "Company_Name": "extract company name here",\n'
                '  "Job_Description": "extract job description here",\n'
                '  "Key_Responsibilities": "extract responsibilities here",\n'
                '  "Qualifications_and_Requirements": "extract requirements here",\n'
                '  "Location": "extract location here",\n'
                '  "Benefits_Salary": "extract benefits here",\n'
                '  "Company_Overview": "extract company info here"\n'
                "}}\n\n"
                "RETURN ONLY THE JSON OBJECT ABOVE WITH EXTRACTED VALUES. NO OTHER TEXT."
            ),
            expected_output=(
                "A valid JSON object with exactly these 8 fields:\n"
                "{\n"
                '  "Job_Title": "exact title from posting or \'Information not available\'",\n'
                '  "Company_Name": "actual company name or \'Information not available\'",\n'
                '  "Job_Description": "summary from posting or \'Information not available\'",\n'
                '  "Key_Responsibilities": "duties listed or \'Information not available\'",\n'
                '  "Qualifications_and_Requirements": "requirements listed or \'Information not available\'",\n'
                '  "Location": "work location or \'Information not available\'",\n'
                '  "Benefits_Salary": "compensation info or \'Information not available\'",\n'
                '  "Company_Overview": "company info or \'Information not available\'"\n'
                "}\n"
                "The response must be valid JSON that can be parsed."
            ),
            # output_pydantic=JobDescription,  # Disabled - using manual parsing
            # output_file="job_description.json",
            agent=agent,
        )

    @staticmethod
    def create_client_profile_task(agent):
        return Task(
            description=(
                "Analyze the client's background and create a comprehensive professional profile. Follow these steps:\n\n"
                "STEP 1: Review the client's resume content:\n"
                "{resumeContent}\n\n"
                "STEP 2: Review the client's personal statement:\n"
                "{Personal_Statement}\n\n"
                "STEP 3: Structure your output in this EXACT ORDER:\n\n"
                "**FIRST: Job Alignment Summary**\n"
                "Create a section titled '## Job Alignment Summary' at the TOP of your response that explains:\n"
                "- How the client's skills match the job requirements\n"
                "- Relevant experiences that make her a strong candidate\n"
                "- Areas where she demonstrates the qualifications sought\n"
                "- Why she would be a good fit for this specific role\n\n"
                "**THEN: Detailed Professional Profile**\n"
                "Follow with the comprehensive profile sections in this order:\n"
                "- Personal Information and Contact Details\n"
                "- Educational Background\n"
                "- Technical Skills and Competencies\n"
                "- Professional Experience and Key Projects\n"
                "- Achievements and Contributions\n"
                "- Languages and Certifications\n"
                "- Interests and Additional Qualifications\n\n"
                "Use markdown formatting for better readability. Write in a professional but engaging tone."
            ),
            expected_output=(
                "A comprehensive professional profile document in markdown format with this EXACT structure:\n"
                "1. ## Job Alignment Summary (FIRST - at the top)\n"
                "2. ## Personal Information and Contact Details\n"
                "3. ## Educational Background\n"
                "4. ## Technical Skills and Competencies\n"
                "5. ## Professional Experience and Key Projects\n"
                "6. ## Achievements and Contributions\n"
                "7. ## Languages and Certifications\n"
                "8. ## Interests and Additional Qualifications\n"
                "All sections should use proper markdown headings and professional formatting."
            ),
            agent=agent,
            output_file="client_profile.md",
        )

    @staticmethod
    def create_company_research_task(agent, job_task):
        return Task(
            description=(
                "Compile a structured summary of the company {comp_name}, including key information such as:"
                "The company's core business, products, or services"
                "The company's location"
                "The company's kununu score, reputation overall employee reviews"
                "Utilize tools to search this company, and visit the first 5 websites of serper result, output the serper result, run web scraping on those websites"
                "Then summarize information collected from those websites and output them in markdown format"
                "Company size, structure and number of employees"
                "If you can find some of the key information, don't fake it just say you can't find it"
                "Use the original language of the job posting."
            ),
            expected_output=(
                "A clear and well structured summary of the company, including key information such as:"
                "The company's core business, products, or services"
                "The company's position. If there are multiple list all of them"
                "The company's kununu score, reputation overall employee reviews"
                "Financial stability and growth"
                "Company size, structure and number of employees"
            ),
            agent=agent,
            context=[job_task],
            output_json=CompInfo,
            output_file="company_profile.json",
        )

    @staticmethod
    def create_resume_refinement_task(agent, client_task, job_task):
        return Task(
            description=(
                "Refine, rewrite, extend, modify or restructure your client's resume {resumeContent} to improve her chance to get the job."
                "Make use of information provided by ClientKnower to tailor her resume for the job, highlighting her skills and experiences most relevant to that position."
                "If the client's experience or ability align with job requirement, use keywords from the job posting to help her resume pass applicant tracking systems (ATS)."
                "Here are the principles of how you should improve her resume:"
                "1. Make sure the information of client that align with the job's requirement is prioritized in the resume."
                "2. Make use of information provided by ClientKnower to make the resume comprehensive"
                "3. Use action verbs and concrete examples rather than vague statements"
                "4. Use a clean, professional font and formatting that is easy to read"
                "5. Proofread carefully for any errors or typos"
                "6. Do not fake any information that is not true about the client"
                "7. Use the original language of the job posting."
                "8. Use markdown formatting for better readability."
            ),
            expected_output=(
                "A comprehensive and well structured resume document in markdown format"
                "using the original resume overall structure and text style."
                "Complemented with any additional background information that are align with the position requirement."
                "With the most relevant experience or ability prioritized in each section."
            ),
            agent=agent,
            context=[client_task, job_task],
            output_file="refined_resume.md",
        )

    @staticmethod
    def create_cover_letter_task(agent, client_task, job_task):
        return Task(
            description=(
                "You must write a complete German cover letter (Anschreiben) for the job position. Follow these steps:\n\n"
                "STEP 1: Review the client's resume content:\n"
                "{resumeContent}\n\n"
                "STEP 2: Review the client's motivation:\n"
                "{Motivation}\n\n"
                "STEP 3: Write a professional German cover letter that includes:\n"
                "- Header with client's real contact information (name, address, email, phone)\n"
                "- Date: Use EXACTLY this date: {current_date} (format: DD.MM.YYYY). Do NOT use any other date.\n"
                "- Company address (if available)\n"
                "- Professional greeting: 'Sehr geehrte Damen und Herren'\n"
                "- Opening paragraph introducing the specific job position\n"
                "- Body paragraphs incorporating the client's motivation and relevant qualifications\n"
                "- Closing paragraph with availability and interview request\n"
                "- Professional sign-off: 'Mit freundlichen Grüßen'\n"
                "- Client's signature line\n\n"
                "CRITICAL REQUIREMENTS:\n"
                "- Write the COMPLETE cover letter text, not just promises or descriptions\n"
                "- Use ONLY real information from the resume provided above\n"
                "- Include the client's actual motivation provided above\n"
                "- Write in professional German language\n"
                "- NO disclaimers, notes, or sample text\n"
                "- NO separator lines (---) or explanatory text\n"
                "- Provide ONLY the actual cover letter content ready to send"
            ),
            expected_output=(
                "A complete, professional German cover letter (Anschreiben) with this exact structure:\n"
                "1. Complete header with client's real contact information\n"
                "2. Date and company information\n"
                "3. Salutation: 'Sehr geehrte Damen und Herren'\n"
                "4. Complete body paragraphs with motivation and qualifications\n"
                "5. Professional closing: 'Mit freundlichen Grüßen'\n"
                "6. Signature line with client's name\n"
                "Must be ready to send with NO additional text, disclaimers, or explanations."
            ),
            agent=agent,
            context=[client_task, job_task],
            output_file="cover_letter.md",
        )

    @staticmethod
    def create_fact_check_task(agent, client_task, job_task, cover_letter_task):
        return Task(
            description=(
                "Review the generated cover letter, check whether its stated facts are true as written in her resume content: {resumeContent}. "
                "Remove all parts that are not true about her, keep only the true parts. "
                "If the cover letter becomes shorter than half page after removal, pick some relevant experience from her resume content {resumeContent} to complete the cover letter. "
                "Most importantly, only use information from her resume content: {resumeContent}, do not fake any experience that is not in her resume. "
                "Make sure all information from her {Motivation} are included. "
                "Work directly with the resume content provided in the resumeContent variable."
            ),
            expected_output=(
                "A well-crafted, half to one page cover letter in markdown format that:"
                "- Is tailored to the specific job and company, while maintaining the truthfulness of her experience stated in the cover letter"
                "- Highlights the client's most relevant qualifications"
                "- Incorporate her motivation: {Motivation} for the job"
                "- Uses a professional but easily understandable tone"
                "- Incorporates relevant keywords from the job posting"
                "- Is free of errors and typos"
            ),
            agent=agent,
            context=[client_task, job_task, cover_letter_task],
            output_file="cover_letter_checked.md",
        )
