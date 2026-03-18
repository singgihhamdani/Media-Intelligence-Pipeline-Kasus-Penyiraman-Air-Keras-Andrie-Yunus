import pandas as pd
from gnews import GNews
import os

def fetch_news(query: str, max_results: int) -> pd.DataFrame:
    """
    Fetch news articles using GNews.
    
    Args:
        query (str): The search query.
        max_results (int): Maximum number of articles to retrieve.
        
    Returns:
        pd.DataFrame: DataFrame containing fetched news.
    """
    print(f"Fetching news for query: '{query}' (Max: {max_results})...")
    google_news = GNews(language='id', country='ID', max_results=max_results)
    articles = google_news.get_news(query)
    
    if not articles:
        print("No articles found.")
        return pd.DataFrame(columns=['title', 'published_date', 'source', 'url'])
    
    # Extract relevant fields
    formatted_articles = []
    for article in articles:
        publisher = article.get('publisher', '')
        source_name = publisher.get('title', '') if isinstance(publisher, dict) else str(publisher)
        
        formatted_articles.append({
            'title': article.get('title', ''),
            'published_date': article.get('published date', ''),
            'source': source_name,
            'url': article.get('url', '')
        })
        
    df = pd.DataFrame(formatted_articles)
    print(f"Retrieved {len(df)} articles.")
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save raw data
    output_path = 'data/raw_news.csv'
    df.to_csv(output_path, index=False)
    print(f"Saved raw articles to {output_path}")
    
    return df
