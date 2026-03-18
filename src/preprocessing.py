import pandas as pd
import numpy as np
import os

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the raw news data.
    """
    print("Preprocessing data...")
    if df.empty:
        print("Empty DataFrame received for preprocessing.")
        return df
        
    # Convert published_date to datetime reliably, handle timezones
    df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce', utc=True)
    df['published_date'] = df['published_date'].dt.tz_localize(None)
    
    # Drop rows where date couldn't be parsed
    initial_len = len(df)
    df = df.dropna(subset=['published_date']).copy()
    if len(df) < initial_len:
         print(f"Dropped {initial_len - len(df)} rows with invalid dates.")
         
    # Create date_only column as normalized datetime object (to start of day)
    df['date_only'] = df['published_date'].dt.normalize()
    
    # Force Date Filtering bounds (March 7th - 17th)
    start_date = pd.to_datetime('2026-03-07')
    end_date = pd.to_datetime('2026-03-17')
    df = df[(df['date_only'] >= start_date) & (df['date_only'] <= end_date)].copy()
    
    # Normalize title text (lowercase)
    df['title'] = df['title'].str.lower()
    
    # Remove duplicate titles
    initial_len = len(df)
    df = df.drop_duplicates(subset=['title'], keep='first').copy()
    print(f"Removed {initial_len - len(df)} duplicate articles.")
    
    # Handle other missing values
    df = df.fillna('')
    
    # Sort by date
    df = df.sort_values('published_date').reset_index(drop=True)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save clean data
    output_path = 'data/clean_news.csv'
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} clean articles to {output_path}")
    
    return df
