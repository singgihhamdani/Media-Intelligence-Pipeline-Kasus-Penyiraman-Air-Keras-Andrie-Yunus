import pandas as pd
import numpy as np
from collections import Counter
from typing import Dict, Any

def daily_news_volume(df: pd.DataFrame) -> pd.DataFrame:
    """Count total news per day."""
    if df.empty:
        return pd.DataFrame(columns=['date_only', 'total_volume'])
    
    volume = df.groupby('date_only').size().reset_index(name='total_volume')
    return volume

def daily_case_volume(df: pd.DataFrame) -> pd.DataFrame:
    """Count case-related news per day."""
    if df.empty or 'is_case_news' not in df.columns:
        return pd.DataFrame(columns=['date_only', 'case_volume'])
        
    case_df = df[df['is_case_news'] == 1]
    volume = case_df.groupby('date_only').size().reset_index(name='case_volume')
    return volume

def share_of_voice(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate case_news / total_news per day."""
    total_vol = daily_news_volume(df)
    case_vol = daily_case_volume(df)
    
    if total_vol.empty:
        return pd.DataFrame(columns=['date_only', 'total_volume', 'case_volume', 'share_of_voice'])
        
    merged = pd.merge(total_vol, case_vol, on='date_only', how='left')
    merged['case_volume'] = merged['case_volume'].fillna(0)
    merged['share_of_voice'] = (merged['case_volume'] / merged['total_volume']).fillna(0)
    
    return merged

def _get_ngrams(text: str, n: int, list_stopwords: set) -> list:
    """Generate n-grams from text."""
    clean_title = ''.join(c if c.isalnum() else ' ' for c in str(text))
    tokens = [w for w in clean_title.split() if len(w) > 2 and w not in list_stopwords]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def keyword_analysis(df: pd.DataFrame, top_n: int = 10, ngram_range: tuple = (1, 2)) -> pd.DataFrame:
    """Find most frequent words/phrases with Sub-string Consolidation."""
    if df.empty:
        return pd.DataFrame(columns=['keyword', 'count'])
        
    stopwords = {'dan', 'di', 'yang', 'untuk', 'pada', 'ke', 'dari', 'ini', 'itu', 'dengan', 
                 'dalam', 'akan', 'juga', 'oleh', 'tak', 'tidak', 'ada', 'sebagai', 'sudah', 
                 'bisa', 'karena', 'kasus', 'tentang', 'saat', 'setelah', 'hari', 'tahun', '-', '|',
                 'indonesia', 'lebih', 'bagi', 'atau', 'jadi', 'buat', 'lalu', 'baru', 'hingga'}
                 
    all_ngrams = []
    for title in df['title'].values:
        for n in range(ngram_range[0], ngram_range[1] + 1):
            all_ngrams.extend(_get_ngrams(title, n, stopwords))
            
    counter = Counter(all_ngrams)
    valid_ngrams = {k: v for k,v in counter.items() if len(k) > 4}
    
    # Sub-string consolidation
    sorted_phrases = sorted(valid_ngrams.keys(), key=len, reverse=True)
    consolidated = {}
    
    for phrase in sorted_phrases:
        count = valid_ngrams[phrase]
        is_substring = False
        for kept_phrase in consolidated.keys():
            # If it's a substring and doesn't appear significantly more often than its parent, amalgamate it
            if phrase in kept_phrase and count <= (consolidated[kept_phrase] * 1.5):
                is_substring = True
                break
        if not is_substring:
            consolidated[phrase] = count
            
    most_common = Counter(consolidated).most_common(top_n)
    return pd.DataFrame(most_common, columns=['keyword', 'count'])

def source_analysis(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Analyze top publishers/sources for the narrative."""
    if df.empty or 'source' not in df.columns:
        return pd.DataFrame(columns=['source', 'count'])
    
    counts = df['source'].value_counts().reset_index()
    counts.columns = ['source', 'count']
    counts = counts[counts['source'] != '']
    return counts.head(top_n)

def find_patient_zero(df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """Find the earliest publishers (Patient Zero) that broke the news."""
    if df.empty or 'published_date' not in df.columns:
        return pd.DataFrame(columns=['published_date', 'source', 'title'])
        
    earliest = df.sort_values('published_date', ascending=True)
    # Ensure source isn't blank
    earliest = earliest[earliest['source'] != '']
    return earliest[['published_date', 'source', 'title']].head(top_n)

def anomaly_detection(df_volume: pd.DataFrame, column: str = 'case_volume', threshold: float = 2.0, event_date: str = '2026-03-12') -> pd.DataFrame:
    """Use z-score to detect abnormal spikes/drops in volume."""
    if df_volume.empty or len(df_volume) < 2:
        df_volume['z_score'] = 0
        df_volume['is_anomaly'] = False
        return df_volume
        
    if event_date:
        event_dt = pd.to_datetime(event_date)
        pre_event = df_volume[df_volume['date_only'] < event_dt]
        
        if len(pre_event) > 1 and pre_event[column].std() > 0:
            mean = pre_event[column].mean()
            std = pre_event[column].std()
        else:
            mean = df_volume[column].mean()
            std = df_volume[column].std()
    else:
        mean = df_volume[column].mean()
        std = df_volume[column].std()
        
    if std == 0:
        df_volume['z_score'] = 0
        df_volume['is_anomaly'] = False
        return df_volume
        
    df_volume['z_score'] = (df_volume[column] - mean) / std
    df_volume['is_anomaly'] = df_volume['z_score'].abs() > threshold
    
    return df_volume

def moving_average(df_volume: pd.DataFrame, column: str = 'case_volume', window: int = 3) -> pd.DataFrame:
    """Smooth trends using rolling average."""
    if df_volume.empty or len(df_volume) < window:
        df_volume[f'{column}_ma{window}'] = df_volume[column] if column in df_volume else 0
        return df_volume
        
    df_volume[f'{column}_ma{window}'] = df_volume[column].rolling(window=window, min_periods=1).mean()
    return df_volume
