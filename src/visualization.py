import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os

def set_style():
    """Set the plotting style for consistency."""
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.labelsize'] = 14

def _finalize_plot(save_path: str = None):
    # Common helper to display or save
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to {save_path}")
        plt.close()
    else:
        plt.show()

def plot_daily_volume(sov_df: pd.DataFrame, save_path: str = None):
    """Line chart for daily case news volume and moving average."""
    if sov_df.empty:
        print("No data for daily volume plot.")
        return
        
    set_style()
    fig, ax = plt.subplots()
    
    # Ensure proper datetime objects
    sov_df = sov_df.copy()
    sov_df['date_only'] = pd.to_datetime(sov_df['date_only'])
    
    sns.lineplot(data=sov_df, x='date_only', y='case_volume', marker='o', ax=ax, label='Daily Volume')
    if 'case_volume_ma3' in sov_df.columns:
        sns.lineplot(data=sov_df, x='date_only', y='case_volume_ma3', linestyle='--', ax=ax, label='3-Day MA')
        
    # Mark anomalies
    if 'is_anomaly' in sov_df.columns:
        anomalies = sov_df[sov_df['is_anomaly']]
        if not anomalies.empty:
            ax.scatter(anomalies['date_only'], anomalies['case_volume'], color='red', s=100, zorder=5, label='Anomaly (Spike)')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.title("Daily Case News Volume over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Articles")
    plt.xticks(rotation=45)
    plt.legend()
    
    _finalize_plot(save_path)

def plot_share_of_voice(sov_df: pd.DataFrame, save_path: str = None):
    """Line chart for share of voice over time."""
    if sov_df.empty:
        print("No data for share of voice plot.")
        return
        
    set_style()
    fig, ax = plt.subplots()
    
    sov_df = sov_df.copy()
    sov_df['date_only'] = pd.to_datetime(sov_df['date_only'])
    
    sns.lineplot(data=sov_df, x='date_only', y='share_of_voice', marker='s', color='purple', ax=ax)
    ax.fill_between(sov_df['date_only'], sov_df['share_of_voice'], alpha=0.2, color='purple')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Format y-axis percentage robustly
    if len(ax.get_yticks()) > 0:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    
    plt.title("Share of Voice: Target Case vs Competing Baseline")
    plt.xlabel("Date")
    plt.ylabel("Share of Voice (%)")
    plt.xticks(rotation=45)
    
    _finalize_plot(save_path)

def plot_top_keywords(keywords_df: pd.DataFrame, save_path: str = None):
    """Bar chart for top phrases/ngrams."""
    if keywords_df.empty:
        print("No data for phrases plot.")
        return
        
    set_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.barplot(data=keywords_df, y='keyword', x='count', hue='keyword', legend=False, palette='viridis', ax=ax)
    
    plt.title(f"Top {len(keywords_df)} Narrative Phrases in Case News Titles")
    plt.xlabel("Frequency")
    plt.ylabel("Phrase")
    
    _finalize_plot(save_path)

def plot_top_sources(sources_df: pd.DataFrame, save_path: str = None):
    """Bar chart for top publishers."""
    if sources_df.empty:
        print("No data for sources plot.")
        return
        
    set_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.barplot(data=sources_df, y='source', x='count', hue='source', legend=False, palette='magma', ax=ax)
    
    plt.title(f"Top {len(sources_df)} Amplifying Media Sources")
    plt.xlabel("Number of Articles")
    plt.ylabel("Publisher")
    
    _finalize_plot(save_path)
