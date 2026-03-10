import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import RequestException
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# Import search tools with fallbacks
try:
    from crewai_tools import SerperDevTool
except ImportError:
    SerperDevTool = None

try:
    from crewai_tools import DuckDuckGoSearchRun
except ImportError:
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
    except ImportError:
        DuckDuckGoSearchRun = None

# Create proper CrewAI tools
class WebScrapingInput(BaseModel):
    """Input for web scraping tool."""
    url: str = Field(description="URL to scrape")

class WebScrapingTool(BaseTool):
    name: str = "web_scraper"
    description: str = "Scrape text content from a web page URL"
    args_schema: Type[BaseModel] = WebScrapingInput

    def _run(self, url: str) -> str:
        """Execute the web scraping."""
        def exponential_backoff(attempt):
            return min(60, 30 * (2 ** attempt))

        for attempt in range(3):
            try:
                timeout = exponential_backoff(attempt)
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup.get_text()
            except RequestException as e:
                if attempt == 2:  # Last attempt
                    return f"Error scraping the website after 3 attempts: {str(e)}"
                print(f"Attempt {attempt + 1} failed. Retrying in {timeout} seconds...")
                time.sleep(timeout)
        
        return "Failed to scrape the website"

class WebScrapingTools:
    @staticmethod
    def get_web_scraper():
        """Get the web scraper tool"""
        return WebScrapingTool()

class FileReaderInput(BaseModel):
    """Input for file reading tool."""
    file_path: str = Field(description="Path to the file to read")

class FileReaderTool(BaseTool):
    name: str = "file_reader"
    description: str = "Read content from a file"
    args_schema: Type[BaseModel] = FileReaderInput

    def _run(self, file_path: str) -> str:
        """Execute the file reading."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            return f"Error: File not found at {file_path}"
        except IOError:
            return f"Error: Unable to read file at {file_path}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

class FileTools:
    @staticmethod
    def get_file_reader():
        """Get the file reader tool"""
        return FileReaderTool()

class SearchTools:
    def __init__(self):
        self.search_tool = DuckDuckGoSearchRun() if DuckDuckGoSearchRun else None
        self.serper_tool = SerperDevTool() if (SerperDevTool and os.getenv('SERPER_API_KEY')) else None
    
    def get_search_tool(self):
        return self.search_tool
    
    def get_serper_tool(self):
        return self.serper_tool