from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import io
from backend.models import JobApplicationRequest, JobApplicationResponse
from backend.anschreiben_service import AnschreibenService
from backend.pdf_service import generate_cover_letter_pdf

# Import for file processing
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None


def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF content"""
    if not PyPDF2:
        raise HTTPException(
            status_code=400, detail="PDF support not available. Please install PyPDF2."
        )

    try:
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF file: {str(e)}")


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX content"""
    if not Document:
        raise HTTPException(
            status_code=400,
            detail="DOCX support not available. Please install python-docx.",
        )

    try:
        docx_file = io.BytesIO(content)
        doc = Document(docx_file)

        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error reading DOCX file: {str(e)}"
        )


app = FastAPI(
    title="Anschreiben Generator",
    description="AI-powered cover letter generation service",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create outputs directory if it doesn't exist
os.makedirs("outputs", exist_ok=True)
os.makedirs("frontend", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/icon", StaticFiles(directory="icon"), name="icon")

# Initialize service
service = AnschreibenService()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main application page"""
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(
            content=content,
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
    except FileNotFoundError:
        return HTMLResponse(
            """
        <html>
            <head><title>Anschreiben Generator</title></head>
            <body>
                <h1>Anschreiben Generator</h1>
                <p>Frontend not found. Please check frontend/index.html</p>
                <p>Use the API endpoints:</p>
                <ul>
                    <li>POST /generate - Generate basic cover letter</li>
                    <li>POST /generate-full - Generate with company research</li>
                    <li>GET /docs - API documentation</li>
                </ul>
            </body>
        </html>
        """
        )


@app.post("/generate", response_model=JobApplicationResponse)
async def generate_cover_letter(
    posting_url: str = Form(..., description="Job posting URL"),
    resume_content: str = Form(..., description="Resume content"),
    motivation: str = Form(..., description="Motivation for the job"),
    personal_statement: str = Form("", description="Personal statement (optional)"),
):
    """Generate basic cover letter with job analysis and client profiling"""
    try:
        request = JobApplicationRequest(
            posting_url=posting_url,
            resume_content=resume_content,
            motivation=motivation,
            personal_statement=personal_statement,
        )

        result = service.generate_application_materials(request)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating cover letter: {str(e)}"
        )


@app.post("/generate-full", response_model=JobApplicationResponse)
async def generate_full_application(
    posting_url: str = Form(..., description="Job posting URL"),
    resume_content: str = Form(..., description="Resume content"),
    motivation: str = Form(..., description="Motivation for the job"),
    personal_statement: str = Form("", description="Personal statement (optional)"),
):
    """Generate complete application materials with company research and resume optimization"""
    try:
        request = JobApplicationRequest(
            posting_url=posting_url,
            resume_content=resume_content,
            motivation=motivation,
            personal_statement=personal_statement,
        )

        result = service.generate_application_materials(request)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating full application: {str(e)}"
        )


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and read resume file"""
    try:
        # Read file content
        content = await file.read()
        filename = file.filename.lower()

        # Handle different file types
        if filename.endswith(".pdf"):
            text_content = extract_text_from_pdf(content)
        elif filename.endswith(".docx"):
            text_content = extract_text_from_docx(content)
        elif filename.endswith(".doc"):
            raise HTTPException(
                status_code=400,
                detail="DOC files are not supported. Please convert to DOCX or PDF format.",
            )
        else:
            # Handle text files
            try:
                text_content = content.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    text_content = content.decode("latin-1")
                except UnicodeDecodeError:
                    raise HTTPException(
                        status_code=400,
                        detail="Unable to decode file. Please upload a text, PDF, or DOCX file.",
                    )

        if not text_content.strip():
            raise HTTPException(
                status_code=400,
                detail="File appears to be empty or could not extract text.",
            )

        return {"filename": file.filename, "content": text_content}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.post("/download-pdf")
async def download_cover_letter_pdf(
    cover_letter: str = Form(..., description="Cover letter text"),
):
    """Generate a PDF from the cover letter text and return it as a download."""
    try:
        pdf_bytes = generate_cover_letter_pdf(cover_letter)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=Anschreiben.pdf"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Anschreiben Generator is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
