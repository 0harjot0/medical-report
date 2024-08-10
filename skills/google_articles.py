from typing import List
import requests
import os
from xml.etree import ElementTree
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from typing import List, Dict
load_dotenv()


def get_medical_articles_full_text(condition: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Retrieves medical articles related to a specific condition, including full text of each article.

    Args:
        condition: str - The medical condition to search for.
        num_results: int - The number of search results to retrieve.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing the title, link, snippet, source, and full text of an article.
    """
    api_key = os.getenv('CUSTOM_SEARCH_API')
    if not api_key:
        raise ValueError("CUSTOM_SEARCH_API not found in environment variables")

    base_url = "https://www.googleapis.com/customsearch/v1"
    search_engine_id = "e2048203b30a14a98"  # Your public custom search engine ID

    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": condition,
        "num": num_results
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return []
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode the API response as JSON")
        return []
    
    articles = []
    items = search_results.get("items", [])
    if not items:
        print("No search results found or 'items' key missing in the response")
        return []
    
    for item in items:
        if isinstance(item, dict):
            title = item.get("title", "No title available")
            link = item.get("link", "")
            snippet = item.get("snippet", "No snippet available")
            source = item.get("displayLink", "Unknown source")
            
            # Extract full article text using BeautifulSoup with modified User-Agent
            full_text = extract_full_text(link)
            if not full_text:
                full_text = "Full text could not be extracted."
            
            articles.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "source": source,
                "full_text": full_text
            })
        else:
            print(f"Unexpected item format: {item}")
    
    return articles

def extract_full_text(url: str) -> str:
    """
    Extracts full text from a given URL using BeautifulSoup.

    Args:
        url: str - The URL of the article.

    Returns:
        str: The full text of the article.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracting all paragraphs and joining them into a single string
        paragraphs = soup.find_all('p')
        full_text = ' '.join([para.get_text() for para in paragraphs])
        return full_text.strip()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while extracting the article from {url}: {e}")
        return "Full text could not be extracted."



# condition = "diabetes"
# articles = get_medical_articles_full_text(condition)

# if articles:
#     for article in articles:
#         print(f"Title: {article['title']}")
#         print(f"Source: {article['source']}")
#         print(f"Link: {article['link']}")
#         print(f"Snippet: {article['snippet']}")
#         print(f"Full Text: {article['full_text'][:500]}...")  # Print first 500 characters of full text
#         print("\n")
# else:
#     print("No articles found or an error occurred.")