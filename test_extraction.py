#!/usr/bin/env python3

import sys
sys.path.append('/mnt/c/Users/Lan.Yang/Projekten2025/CC')

from backend.anschreiben_service import AnschreibenService

def test_url_extraction(url):
    """Test URL extraction to see what content is being extracted"""
    service = AnschreibenService()
    
    print(f"Testing URL extraction for: {url}")
    print("=" * 80)
    
    content = service._extract_url_content(url)
    
    print(f"Extracted content length: {len(content)}")
    print(f"Content type: {type(content)}")
    print("First 500 characters:")
    print("-" * 40)
    print(content[:500])
    print("-" * 40)
    print("Last 500 characters:")
    print(content[-500:])
    print("=" * 80)
    
    # Check for common indicators of failed extraction
    indicators = ["Error scraping", "Failed to scrape", "JavaScript", "cookies", "blocked"]
    for indicator in indicators:
        if indicator.lower() in content.lower():
            print(f"WARNING: Found '{indicator}' in content - possible extraction issue")
    
    if len(content.strip()) < 100:
        print("WARNING: Content is very short - possible extraction failure")
    
    return content

if __name__ == "__main__":
    # Test with a common job posting URL format
    test_url = input("Enter a job posting URL to test: ").strip()
    if test_url:
        test_url_extraction(test_url)
    else:
        print("No URL provided")