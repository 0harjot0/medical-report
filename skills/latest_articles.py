from typing import List
import requests
import os
from xml.etree import ElementTree
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def latest_medical_research(condition: str) -> List[dict]:
    """
    Retrieves latest medical research articles associated with a specific medical condition.
    The articles are sorted by relevance.

    Args:
        condition: str - The medical condition or disease to search for

    Returns:
        List[dict]: latest medical research articles with relevance scores and publication details
    """
    api_key = os.getenv("NCBI_API_KEY")
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    # Search for articles
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={condition}&retmax=1&sort=relevance&apikey={api_key}"
    search_response = requests.get(search_url)
    search_root = ElementTree.fromstring(search_response.content)
    
    id_list = [id_elem.text for id_elem in search_root.findall(".//Id")]
    
    # Fetch details for each article
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(id_list)}&retmode=xml&apikey={api_key}"
    fetch_response = requests.get(fetch_url)
    fetch_root = ElementTree.fromstring(fetch_response.content)
    
    articles = []
    for article in fetch_root.findall(".//PubmedArticle"):
        try:
            title = article.find(".//ArticleTitle").text
            abstract = article.find(".//Abstract/AbstractText")
            abstract_text = abstract.text if abstract is not None else "Abstract not available"
            pub_date = article.find(".//PubDate")
            year = pub_date.find("Year").text if pub_date.find("Year") is not None else "Unknown"
            month = pub_date.find("Month").text if pub_date.find("Month") is not None else "Unknown"
            
            # Calculate a simple relevance score based on the appearance of the condition in the title and abstract
            relevance_score = (title.lower().count(condition.lower()) * 2 + 
                               abstract_text.lower().count(condition.lower())) / 10
            
            articles.append({
                "title": title,
                "abstract": abstract_text,
                "publication_date": f"{year} {month}",
                "relevance_score": round(relevance_score, 2)
            })
        except AttributeError:
            continue  # Skip articles with missing information
    
    return sorted(articles, key=lambda x: x['relevance_score'], reverse=True)

# Example usage:
# research_articles = latest_medical_research("type 2 diabetes")
# for article in research_articles:
#     print(f"Title: {article['title']}")
#     print(f"Abstract: {article['abstract']}")
#     print(f"Publication Date: {article['publication_date']}")
#     print(f"Relevance Score: {article['relevance_score']}")
#     print("---")

