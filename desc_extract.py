import requests
from bs4 import BeautifulSoup

class JobDescriptionExtractor:
    def __init__(self):
        pass

    def extract_page_text(self, url):
        """
        Fetches the main visible text content from a web page (without any pattern filtering).
        Returns the extracted text as a string.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            # Get text and clean up
            text = soup.get_text(separator='\n')
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            return '\n'.join(lines)
        except Exception as e:
            return f"Error fetching or parsing {url}: {e}"
