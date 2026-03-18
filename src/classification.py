import pandas as pd
from typing import Tuple

def classify_case_news(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Classify news articles based on specific keywords related to the case.
    
    Returns:
        Tuple containing (original_df_with_flag, case_news_df, non_case_news_df)
    """
    print("Classifying case news...")
    if df.empty:
        return df, pd.DataFrame(), pd.DataFrame()
        
    keywords = ["andrie yunus", "penyiraman", "air keras", "kontras"]
    
    # Create is_case_news column (1 if title contains any keyword, else 0)
    # The title column is already lowercased in the preprocessing step
    pattern = '|'.join(keywords)
    df['is_case_news'] = df['title'].str.contains(pattern, case=False, na=False).astype(int)
    
    # Split into case_news and non_case_news
    case_news = df[df['is_case_news'] == 1].copy()
    non_case_news = df[df['is_case_news'] == 0].copy()
    
    print(f"Classification complete: {len(case_news)} case-related and {len(non_case_news)} non-related news items.")
    
    return df, case_news, non_case_news
