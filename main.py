import os
import pandas as pd
from src import scraper, preprocessing, classification, analysis, visualization

def main():
    print("=======================================")
    print("  Media Intelligence Analysis Pipeline ")
    print("=======================================\n")
    
    print("Fetching target case news (multiple variants)...")
    queries = ["Andrie Yunus", "Aktivis KontraS", "Disiram Air Keras"]
    target_dfs = []
    
    for q in queries:
        df_q = scraper.fetch_news(q, max_results=300)
        target_dfs.append(df_q)
        
    df_target = pd.concat(target_dfs, ignore_index=True)
    
    print("Fetching baseline news (competing national issues)...")
    baseline_queries = ["Hak Angket", "Harga Beras"]
    baseline_dfs = []
    
    for q in baseline_queries:
        df_q = scraper.fetch_news(q, max_results=300)
        baseline_dfs.append(df_q)
        
    df_baseline = pd.concat(baseline_dfs, ignore_index=True)
    
    if df_target.empty and df_baseline.empty:
        print("Pipeline aborted: No data fetched.")
        return
        
    df_raw = pd.concat([df_target, df_baseline], ignore_index=True)
    
    # 2. Clean Data (Strictly Filtered to March 7-17, 2026)
    df_clean = preprocessing.preprocess_data(df_raw)
    
    # 3. Classify case news
    df_classified, case_news, non_case_news = classification.classify_case_news(df_clean)
    
    # 4. Run Analysis
    print("\nRunning Media Intelligence Analysis...")
    sov_df = analysis.share_of_voice(df_classified)
    
    sov_df = analysis.anomaly_detection(sov_df, column='case_volume', threshold=1.5, event_date='2026-03-12')
    sov_df = analysis.moving_average(sov_df, column='case_volume', window=3)
    
    # Narrative Analysis (Bigrams & Trigrams optimized)
    top_phrases = analysis.keyword_analysis(case_news, top_n=15, ngram_range=(2, 3))
    
    # Source Analysis (Top Publishers)
    top_sources = analysis.source_analysis(case_news, top_n=10)
    
    # Patient Zero (First Publishers)
    patient_zero_df = analysis.find_patient_zero(case_news, top_n=3)
    
    print("Analysis complete.")
    
    # 5. Generate Visualizations
    print("\nGenerating Visualizations...")
    viz_dir = 'notebook/images'
    visualization.plot_daily_volume(sov_df, save_path=f'{viz_dir}/daily_volume.png')
    visualization.plot_share_of_voice(sov_df, save_path=f'{viz_dir}/share_of_voice.png')
    visualization.plot_top_keywords(top_phrases, save_path=f'{viz_dir}/top_phrases.png')
    visualization.plot_top_sources(top_sources, save_path=f'{viz_dir}/top_sources.png')
    
    # 6. Generate Insights
    print("\n=======================================")
    print("           MEDIA INSIGHTS              ")
    print("=======================================")
    
    if not sov_df.empty and sov_df['case_volume'].sum() > 0:
        total_articles = sov_df['case_volume'].sum()
        print(f"📰 Total Case Articles Analyzed: {total_articles}")
        
        # Peak coverage date
        peak_idx = sov_df['case_volume'].idxmax()
        peak_row = sov_df.loc[peak_idx]
        peak_date_str = peak_row['date_only'].strftime('%Y-%m-%d')
        peak_volume = peak_row['case_volume']
        print(f"\n📌 Peak Coverage Date: {peak_date_str} (Articles: {peak_volume})")
        
        # Drop after peak
        post_peak_df = sov_df[sov_df['date_only'] > peak_row['date_only']]
        if not post_peak_df.empty:
            avg_post_peak = post_peak_df['case_volume'].mean()
            drop_pct = ((peak_volume - avg_post_peak) / peak_volume) * 100
            print(f"📉 Average Drop After Peak: {drop_pct:.1f}%")
        else:
            print("📉 Drop After Peak: Insufficient data (peak is at the end of window)")
            
        # Top Phrases Driving Narrative
        if not top_phrases.empty:
            phrases = top_phrases['keyword'].head(3).tolist()
            print(f"🗣️ Top Narrative Phrases: {', '.join(phrases)}")
            
        # Top Amplifiers
        if not top_sources.empty:
            sources = top_sources['source'].head(3).tolist()
            print(f"📢 Top Amplifying Media: {', '.join(sources)}")
            
        # Patient Zero
        if not patient_zero_df.empty:
            print(f"\n🕵️ Patient Zero (Earliest Sources):")
            for idx, row in patient_zero_df.iterrows():
                dt_str = row['published_date'].strftime('%Y-%m-%d %H:%M')
                title_short = (row['title'][:45] + '...') if len(str(row['title'])) > 45 else row['title']
                print(f"   - {dt_str} | {row['source']} | {title_short}")
            
        # Anomalies
        anomalies = sov_df[sov_df['is_anomaly']]
        if not anomalies.empty:
            dates = [d.strftime('%Y-%m-%d') for d in anomalies['date_only']]
            print(f"\n⚠️ Abnormal Spikes Detected On: {', '.join(dates)}")
        else:
            print("\n✅ No abnormal coverage spikes detected.")
            
    else:
        print("\nNot enough case-related news to generate insights.")
        
    print("\n=======================================")
    print("           PIPELINE COMPLETE           ")
    print("=======================================\n")

if __name__ == "__main__":
    for directory in ['data', 'src', 'notebook/images']:
        os.makedirs(directory, exist_ok=True)
    main()
