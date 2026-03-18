# 📊 Media Intelligence Pipeline — Kasus Penyiraman Air Keras Andrie Yunus

Pipeline analisis pemberitaan media berbasis Python untuk mendeteksi pergeseran atensi, anomali volume, dan pola narasi seputar kasus penyiraman air keras terhadap aktivis KontraS Andrie Yunus (12 Maret 2026).

> **Disclaimer:** Proyek ini adalah eksperimen *data science* dan *media intelligence*. Hipotesis strategis yang diajukan didasarkan pada korelasi temporal, bukan kausalitas. Proyek ini tidak bertujuan membuktikan konspirasi.

---

## 🎯 Tujuan

- Mendeteksi perubahan volume pemberitaan sebelum dan sesudah insiden.
- Mengukur *Share of Voice* kasus terhadap isu nasional kompetitor.
- Mengidentifikasi media pertama yang memberitakan (*Patient Zero*).
- Mengekstrak frasa narasi utama yang digunakan jurnalis (*N-Gram Analysis*).
- Mengajukan hipotesis *Strategic Crisis Communication* berdasarkan pola data.

---

## 🏗️ Struktur Proyek

```
berita/
├── data/
│   ├── raw_news.csv              # Data mentah dari Google News
│   └── clean_news.csv            # Data bersih setelah preprocessing
├── src/
│   ├── __init__.py
│   ├── scraper.py                # Pengambilan berita via GNews API
│   ├── preprocessing.py          # Pembersihan, normalisasi, filter tanggal
│   ├── classification.py         # Klasifikasi berita kasus vs baseline
│   ├── analysis.py               # SOV, N-Gram, Patient Zero, Anomaly Detection
│   └── visualization.py          # Grafik siap presentasi (Matplotlib/Seaborn)
├── notebook/
│   ├── analysis.ipynb            # Dashboard interaktif + penjelasan Bahasa Indonesia
│   └── images/                   # Grafik output (.png)
├── main.py                       # Orkestrator pipeline end-to-end
├── artikel_medium.md             # Draft artikel Medium
├── requirements.txt              # Dependensi Python
└── README.md
```

---

## ⚙️ Instalasi & Penggunaan

### Prasyarat
- Python 3.9+
- pip

### Setup

```bash
# Clone repository
git clone https://github.com/<username>/media-intelligence-pipeline.git
cd media-intelligence-pipeline

# Buat virtual environment (opsional, disarankan)
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# Install dependensi
pip install -r requirements.txt
```

### Jalankan Pipeline

```bash
python main.py
```

Pipeline akan otomatis:
1. Menarik berita dari Google News (multi-query)
2. Membersihkan dan memfilter data (7–17 Maret 2026)
3. Mengklasifikasikan berita kasus vs baseline
4. Menjalankan analisis statistik (SOV, Anomaly, N-Gram, Patient Zero)
5. Menghasilkan grafik ke `notebook/images/`
6. Mencetak *Media Insights* ke terminal

### Jelajahi via Jupyter Notebook

```bash
cd notebook
jupyter notebook analysis.ipynb
```

---

## 📈 Contoh Output

### Terminal Insights

```
📰 Total Case Articles Analyzed: 22
📌 Peak Coverage Date: 2026-03-17 (Articles: 9)
📉 Average Drop After Peak: 61.7%
🗣️ Top Narrative Phrases: air keras, andrie yunus, disiram air keras
📢 Top Amplifying Media: detikNews, Tempo.co, Hukumonline
🕵️ Patient Zero (Earliest Sources):
   - 2026-03-13 12:01 | Kompas.id
   - 2026-03-13 21:19 | detikNews
⚠️ Abnormal Spikes Detected On: 2026-03-17
```

### Grafik yang Dihasilkan

| Grafik | Deskripsi |
|--------|-----------|
| `daily_volume.png` | Volume harian + Moving Average + Deteksi Anomali (Z-Score) |
| `share_of_voice.png` | SOV kasus vs isu kompetitor (Hak Angket, Harga Beras) |
| `top_phrases.png` | Top 15 frasa narasi (Bigram/Trigram) |
| `top_sources.png` | Top 10 media amplifikator |

---

## 🧠 Fitur Analitis

| Fitur | Deskripsi |
|-------|-----------|
| **Multi-Query Harvesting** | 3 variasi kata kunci untuk meningkatkan volume sampel |
| **Comparative SOV** | Benchmark terhadap isu kompetitor nyata |
| **N-Gram + Sub-string Consolidation** | Menghilangkan frasa redundan secara otomatis |
| **Patient Zero Tracking** | Identifikasi media pertama yang memberitakan |
| **Anomaly Detection (Z-Score)** | Deteksi lonjakan statistik menggunakan baseline pra-kejadian |
| **Media Fatigue Metric** | Mengukur persentase penurunan volume pasca-puncak |

---

## 📝 Artikel Terkait

Penjelasan lengkap metodologi dan temuan tersedia di artikel Medium:
- [`artikel_medium.md`](artikel_medium.md) — Draft artikel siap publikasi

---

## 🛠️ Tech Stack

- **Bahasa:** Python 3.11
- **Data:** Pandas, NumPy
- **Visualisasi:** Matplotlib, Seaborn
- **Scraping:** GNews
- **Notebook:** Jupyter

---

## ⚠️ Keterbatasan

- Tidak ada analisis sentimen (hanya volume, belum *tone*).
- Tidak mengukur perbincangan di media sosial (X/Twitter).
- Deduplikasi hanya *exact match* (belum *fuzzy matching* untuk sindikasi berita).
- Klasifikasi berita menggunakan *keyword* statis (belum *dynamic topic modeling*).

---

## 📄 Lisensi

Proyek ini dirilis di bawah [MIT License](LICENSE).

---

## 🤝 Kontribusi

*Pull request* dan diskusi sangat terbuka — terutama jika Anda ingin menambahkan:
- Integrasi sentimen (IndoBERT / Hugging Face)
- Scraping media sosial
- Fuzzy string deduplication (TF-IDF Cosine Similarity)
- Dynamic topic modeling (LDA / BERTopic)
