# Anschreiben Generator

An AI-powered application that generates personalized German cover letters (Anschreiben) based on job postings and your resume. This application converts your original Jupyter notebook into a full-featured web application with a modern frontend.

## Features

### Core Functionality
- **Job Posting Analysis**: Extracts key information from job posting URLs
- **Resume Analysis**: Analyzes your resume and creates a comprehensive profile
- **Cover Letter Generation**: Creates tailored cover letters in German or English
- **Fact Checking**: Ensures all information in the cover letter is truthful
- **Company Research**: (Full mode) Researches the company background
- **Resume Optimization**: (Full mode) Optimizes your resume for the specific job

### AI Agents
The application uses CrewAI with specialized agents:
- **PostExtractor**: Analyzes job postings
- **ClientKnower**: Creates comprehensive client profiles
- **CompanyInvestigator**: Researches company information
- **ResumeImprover**: Optimizes resumes for specific jobs
- **CoverLetterWriter**: Generates tailored cover letters
- **FactChecker**: Verifies truthfulness of generated content

## Required Inputs

### Essential Information
1. **Job Posting URL**: The URL of the job you're applying for
2. **Resume Content**: Your current resume (text format)
3. **Motivation**: Your specific motivation and interest in the job

### Optional Information
4. **Personal Statement**: Additional personal information, hobbies, interests

## Setup and Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- (Optional) Serper API key for enhanced company research

### Installation

1. **Clone or setup the project**:
```bash
cd CC
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.example .env
```

Edit `.env` file and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-3.5-turbo
SERPER_API_KEY=your_serper_api_key_here
```

4. **Run the application**:
```bash
python main.py
```

5. **Access the application**:
Open your browser and go to `http://localhost:8000`

## Usage

### Web Interface
1. Open the web application in your browser
2. Fill in the job posting URL
3. Upload your resume file or paste the content
4. Provide your motivation for the job
5. Choose generation mode:
   - **Basic**: Job analysis + Cover letter generation
   - **Full**: Includes company research + resume optimization

### API Endpoints

- `POST /generate`: Generate basic cover letter
- `POST /generate-full`: Generate full application materials
- `POST /upload-resume`: Upload resume files
- `GET /docs`: API documentation
- `GET /health`: Health check

## Project Structure

```
CC/
├── main.py                 # FastAPI application
├── config.py              # Configuration management
├── models.py              # Pydantic models
├── agents.py              # CrewAI agents
├── tasks.py               # CrewAI tasks
├── tools.py               # Web scraping and utility tools
├── anschreiben_service.py # Core service logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── static/
│   └── index.html        # Frontend interface
└── outputs/              # Generated files (created automatically)
```

## Key Improvements from Original

### Code Structure
- ✅ Modular Python files instead of monolithic notebook
- ✅ Proper configuration management
- ✅ Error handling and validation
- ✅ RESTful API design

### User Experience
- ✅ Modern web interface
- ✅ File upload functionality
- ✅ Real-time feedback and progress indication
- ✅ Responsive design for mobile devices

### Functionality
- ✅ Two generation modes (basic vs. full)
- ✅ Session-based output management
- ✅ File upload and text input options
- ✅ Comprehensive error handling

### Technical Features
- ✅ FastAPI backend with automatic documentation
- ✅ Async file handling
- ✅ CORS support for frontend
- ✅ Environment-based configuration

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Troubleshooting

### Common Issues

1. **Missing API Keys**:
   - Ensure `.env` file exists with valid API keys
   - Check that keys are not expired

2. **File Upload Issues**:
   - Ensure uploaded files are text-based (.txt, .md)
   - Check file encoding (UTF-8 preferred)

3. **Generation Timeouts**:
   - Full analysis mode takes longer (3-5 minutes)
   - Check network connectivity
   - Verify API key limits

4. **Missing Dependencies**:
   - Run `pip install -r requirements.txt`
   - Ensure Python version is 3.8+

## Development

To run in development mode with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Contributing

This application is based on your original CrewAI implementation and maintains the same core logic while providing a better user experience through a web interface.