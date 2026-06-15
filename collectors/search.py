"""
Pencarion topik di internet menggunakan Tavily Search API.
"""

from tavily import TavilyClient
from config.settings import TAVILY_API_KEY, MAX_RESULTS_PER_TOPIC

_client = None

def get_client():
    global _client
    if _client is None:
        if not TAVILY_API_KEY:
            raise ValueError(
                "TAVILY_API_KEY not set. Add on file .env"
            )
        _client = TavilyClient(api_key=TAVILY_API_KEY)
    return _client

def search_topic(topic: str, max_results: int = MAX_RESULTS_PER_TOPIC)->list[dict]:

    """
    Searching information on the topics
    
    Returns:
        List of dict, masing-masing berisi:
        -url
        -title
        -content(snippet)
        -raw_content(isi halaman lebig lengkap, jika tersedia)
    """

    client = get_client()
    response = client.search(
        query= topic,
        max_results= max_results,
        include_raw_content= True
    )
    return response.get("results",[])
