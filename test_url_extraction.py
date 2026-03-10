import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import RequestException

def extract_url_content(url: str) -> str:
    """Extract text content from URL using direct web scraping"""
    def exponential_backoff(attempt):
        return min(60, 30 * (2 ** attempt))

    for attempt in range(3):
        try:
            timeout = exponential_backoff(attempt)
            print(f"Attempt {attempt + 1}: Trying to fetch {url}")
            
            # Add headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, timeout=timeout, headers=headers)
            response.raise_for_status()
            print(f"Response status: {response.status_code}")
            print(f"Response length: {len(response.content)} bytes")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text()
            print(f"Extracted text length: {len(text_content)} characters")
            print("First 1000 characters of extracted content:")
            print("-" * 50)
            print(text_content[:1000])
            print("-" * 50)
            return text_content
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == 2:  # Last attempt
                return f"Error scraping the website after 3 attempts: {str(e)}"
            print(f"Retrying in {timeout} seconds...")
            time.sleep(timeout)
    
    return "Failed to scrape the website"

if __name__ == "__main__":
    url = "https://db.recsolu.com/external/requisitions/h5DkdAbfSdh0CsoIekVyjQ"
    content = extract_url_content(url)
    print(f"\nFinal content length: {len(content)} characters")