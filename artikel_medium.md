Saya Membangun Pipeline Media Intelligence dengan Python untuk Membedah Kasus Penyiraman Air Keras Andrie Yunus — Inilah yang Saya Temukan

Sebuah eksperimen data science untuk menganalisis pola pemberitaan media, mendeteksi anomali statistik, dan mengajukan hipotesis komunikasi krisis strategis.

Pada 12 Maret 2026, Andrie Yunus — seorang aktivis dari Komisi untuk Orang Hilang dan Korban Kekerasan (KontraS) — diserang dengan siraman air keras di kawasan Salemba, Jakarta. Kasus ini segera menjadi sorotan media nasional dan internasional.

Sebagai seseorang yang bekerja di persimpangan antara data science dan media intelligence, saya bertanya: Bisakah kita membaca pola di balik pemberitaan ini secara kuantitatif? Bukan untuk membuktikan konspirasi, tetapi untuk mendeteksi:

- Pergeseran atensi media sebelum dan sesudah insiden.
- Lonjakan abnormal (anomaly) dalam volume berita.
- Siapa yang pertama kali menyalakan api pemberitaan (Patient Zero).
- Dan apakah rilis tersangka oleh militer memiliki korelasi dengan puncak tekanan media.

Hasilnya? Saya membangun sebuah pipeline analisis media end-to-end menggunakan Python, dan menemukan pola-pola yang cukup mengejutkan.

🏗️ Arsitektur Pipeline

Sistem ini dibangun secara modular agar bisa direplikasi untuk kasus-kasus lainnya:

project/
├── data/
│   ├── raw_news.csv        # Data mentah dari Google News
│   └── clean_news.csv      # Data bersih setelah preprocessing
├── src/
│   ├── scraper.py           # Pengambilan data via GNews API
│   ├── preprocessing.py     # Pembersihan & normalisasi
│   ├── classification.py    # Klasifikasi berita kasus vs baseline
│   ├── analysis.py          # Analisis statistik & N-Gram
│   └── visualization.py     # Grafik siap presentasi
├── notebook/
│   └── analysis.ipynb       # Dashboard interaktif Jupyter
└── main.py                  # Orkestrator pipeline

Tech Stack: Python, Pandas, NumPy, Matplotlib, Seaborn, GNews.

📡 Strategi Pengambilan Data: Multi-Query Harvesting

Salah satu pelajaran terbesar dari proyek ini: satu kata kunci pencarian tidak cukup.

Ketika saya pertama kali menjalankan pipeline hanya dengan kueri "Andrie Yunus", hasilnya mengecewakan — hanya 6 artikel dalam rentang waktu analisis (7–17 Maret 2026). Sampel sekecil ini tidak memiliki kekuatan statistik apapun.

Solusinya? Multi-Query Harvesting. Saya memperluas pencarian menggunakan tiga variasi kata kunci yang biasa digunakan jurnalis Indonesia untuk menulis tentang kasus ini:

queries = ["Andrie Yunus", "Aktivis KontraS", "Disiram Air Keras"]

Hasilnya dramatis: volume melonjak dari 6 menjadi 22 artikel unik setelah deduplikasi. Ini memberikan fondasi statistik yang jauh lebih solid.

📊 Temuan #1: Anatomi Lonjakan Berita

Grafik di bawah ini memetakan volume berita kasus per hari, lengkap dengan Moving Average (rata-rata bergerak 3 hari) dan deteksi anomali berbasis Z-Score:

(Sisipkan gambar: daily_volume.png)

Apa yang kita lihat:

- 7–11 Maret: Keheningan total. Nol artikel. Media belum menyadari kejadian ini.
- 12 Maret: Hari kejadian. Berita mulai muncul, tetapi lambat — hanya 1–2 artikel.
- 13–14 Maret: Gelombang after-shock. Media nasional mulai berlomba meliput. Volume naik ke 5 artikel per hari.
- 15 Maret (Minggu): Drop drastis ke 2 artikel — efek akhir pekan (Sunday Effect). Redaksi beroperasi dengan kru minimum, dan tidak ada pernyataan resmi baru dari kepolisian.
- 17 Maret: LEDAKAN. Volume melonjak ke 9 artikel — titik merah di grafik menandai ini sebagai Anomali Statistik (Z-Score melampaui threshold). Ini adalah hari di mana polisi mengumumkan bahwa pelaku berjumlah 4 orang.

📈 Temuan #2: Share of Voice — Seberapa Besar Kasus Ini "Mencuri Panggung"?

Share of Voice (SOV) tradisional membandingkan brand Anda dengan kompetitor. Dalam konteks krisis, saya mengadaptasinya untuk mengukur: seberapa besar kasus Andrie Yunus mendominasi atensi media dibandingkan isu nasional lainnya.

Baseline yang saya pilih bukan kueri generik seperti "Indonesia" (yang menghasilkan data tidak relevan), melainkan isu kompetitor nyata yang sedang hangat di periode yang sama:

baseline_queries = ["Hak Angket", "Harga Beras"]

(Sisipkan gambar: share_of_voice.png)

Insight kunci:

- Pada 14 Maret, SOV kasus Andrie Yunus mencapai puncak lebih dari 60% — artinya, dari seluruh berita terkait isu-isu nasional yang kita pantau, lebih dari setengahnya membahas kasus penyiraman air keras ini.
- Ini adalah sinyal merah bagi institusi manapun: sebuah kasus HAM "kecil" berhasil mengalahkan isu elit seperti Hak Angket DPR dalam perebutan atensi publik.

🗣️ Temuan #3: Narasi yang Dipakai Media (N-Gram Analysis)

Alih-alih mengekstrak kata tunggal (yang ambigu), saya membangun algoritma Bigram/Trigram untuk menangkap frasa utuh yang dipakai editor berita di tingkat judul.

Tantangan teknis yang muncul: overlap sub-string. Frasa "disiram air" dan "disiram air keras" dihitung terpisah, padahal maknanya identik. Saya menyelesaikannya dengan algoritma Sub-string Consolidation — jika sebuah Bigram selalu muncul di dalam Trigram induknya, Bigram tersebut otomatis dileburkan.

(Sisipkan gambar: top_phrases.png)

Top 3 frasa narasi:

1. "air keras" — Frasa paling dominan. Media memilih diksi kekerasan fisik, bukan istilah hukum.
2. "andrie yunus" — Nama korban melekat kuat di setiap judul.
3. "disiram air keras" — Konstruksi lengkap yang menggambarkan tindakan serangan.

Implikasi PR: Jika sebuah institusi ingin merespons kasus ini, press release mereka harus menggunakan kosakata yang relevan dengan search intent jurnalis — bukan jargon birokrasi internal.

📢 Temuan #4: Siapa yang Menggoreng dan Siapa yang Memulai?

Top Amplifiers (Volume Terbanyak)

(Sisipkan gambar: top_sources.png)

detikNews memimpin dengan 5 artikel, diikuti oleh Tempo.co dan Hukumonline (masing-masing 3 artikel). Ketiganya adalah Mass Gatekeepers — media yang menjamin isu ini dibaca jutaan orang.

Patient Zero (Media Pertama)

Ini adalah metrik yang paling saya banggakan dalam pipeline ini. Dengan mengurutkan data berdasarkan timestamp publikasi, saya mengidentifikasi media yang pertama kali memecah berita:

- 13 Mar, 12:01 — Kompas.id: "Sebelum disiram air keras, aktivis KontraS…"
- 13 Mar, 21:19 — detikNews: "Aktivis KontraS disiram air keras, Sahroni…"
- 14 Mar, 01:40 — Universitas STK: "Aktivis KontraS Andrie Yunus disiram air keras…"

Kompas.id adalah Patient Zero — media yang menetapkan framing awal di benak publik hampir 9 jam sebelum detikNews mengambil alih narasi dengan volume masifnya.

🕵️ Hipotesis Strategis: "Controlled Release" & Taktik Pengorbanan Bidak

Inilah bagian yang paling kontroversial namun paling menarik secara analitis.

Beberapa hari setelah puncak pemberitaan, diumumkan bahwa 4 prajurit TNI adalah tersangka penyiraman. Pertanyaan kritis yang muncul: Apakah kecepatan rilis ini murni hasil investigasi brilian, atau reaksi panik terhadap tekanan media yang terukur secara statistik?

Tesis: Media-Forced Resolution

Dalam keilmuan Strategic Crisis Communication, fenomena ini dikenal sebagai taktik Containment atau Sacrificing the Pawns (Mengorbankan Bidak):

1. Mematikan Momentum (Deflating the Balloon)

Grafik volume kita menunjukkan kurva yang terus menanjak tanpa tanda-tanda berhenti. Jika dibiarkan, narasi publik berpotensi berevolusi dari "Siapa pelakunya?" menjadi "Ini teror sistematis!"

Menyerahkan 4 nama tersangka memberikan Closure instan. Rasa lapar jurnalis terpuaskan. Kasus berubah dari "Misteri Teror" menjadi sekadar "Sidang Polisi Militer" — sebuah topik yang secara alamiah jauh lebih membosankan bagi editor berita.

2. Melokalisir Kerusakan (Firewalling)

Dengan melabeli tersangka sebagai prajurit tingkat bawah/oknum, fokus media otomatis dialihkan. Tanggung jawab direduksi ke level individu, menyelamatkan reputasi institusi dari badai tuntutan yang lebih besar.

3. Preseden Historis

Bandingkan dengan kasus Novel Baswedan (2017): butuh lebih dari 2,5 tahun untuk mengungkap tersangka penyiraman air keras. Dalam kasus Andrie Yunus, tersangka dirilis dalam hitungan hari. Kecepatan ini, jika dibenturkan dengan puncak Z-Score anomali media, membentuk korelasi temporal yang patut dipertanyakan.

Disclaimer Penting

Hipotesis ini bukan tuduhan. Ini adalah kerangka analitis yang digunakan dalam industri Public Relations dan Crisis Management. Saya tidak memiliki bukti langsung adanya intervensi institusional. Yang saya miliki adalah korelasi temporal antara puncak tekanan media dan kecepatan rilis tersangka — dan korelasi bukanlah kausalitas.

Untuk memverifikasi hipotesis ini, diperlukan data tambahan dari dimensi lain: sentimen media sosial (X/Twitter), analisis jaringan informasi (information network analysis), dan wawancara mendalam dengan jurnalis yang meliput kasus ini.

🔧 Keterbatasan & Pengembangan Selanjutnya

Tidak ada analisis yang sempurna. Berikut adalah titik-titik buta yang saya sadari:

1. Tidak ada Analisis Sentimen. Pipeline saat ini hanya mengukur volume, bukan tone. 100 artikel bernada simpati berbeda maknanya dengan 100 artikel bernada marah.
2. Tidak ada data Media Sosial. Google News hanya menangkap media arus utama. Percakapan publik di X/Twitter — yang seringkali menjadi pemantik awal — tidak terukur.
3. Fuzzy Deduplication belum diterapkan. Banyak portal berita Indonesia yang mempublikasikan ulang artikel yang sama dengan sedikit modifikasi judul (syndication). Deduplikasi exact match saya belum menangkap ini sepenuhnya.
4. Keyword statis. Klasifikasi berita menggunakan daftar kata kunci tetap. Seiring berjalannya narasi (misalnya saat nama tersangka muncul), kata kunci baru harus ditambahkan secara manual.

💡 Lessons Learned

1. Satu kata kunci pencarian tidak pernah cukup. Multi-query harvesting adalah keharusan untuk mendapatkan sampel yang bermakna secara statistik.
2. Baseline harus spesifik. Jangan bandingkan kasus Anda dengan kueri generik seperti "Indonesia". Gunakan isu kompetitor nyata yang sedang berkompetisi di news cycle yang sama.
3. Siapa yang pertama lebih penting dari siapa yang paling banyak. Patient Zero mengatur framing. Amplifier hanya memperbesar volume.
4. Data tanpa konteks adalah angka mati. Drop di hari Minggu bukan sensor media — itu siklus redaksi. Tanpa memahami cara kerja newsroom, kita bisa salah menginterpretasikan pola.

🔗 Kode Sumber

Seluruh kode sumber pipeline ini tersedia secara publik. Anda bisa mereplikasi analisis ini untuk kasus lain hanya dengan mengganti parameter kueri dan rentang tanggal.

Stack: Python 3.11 · Pandas · NumPy · Matplotlib · Seaborn · GNews

Terima kasih sudah membaca. Jika Anda bekerja di bidang PR, jurnalisme, atau advokasi HAM dan tertarik untuk mendiskusikan metodologi ini lebih lanjut, saya terbuka untuk berdiskusi.

Jika artikel ini bermanfaat, silakan tinggalkan clap 👏 dan bagikan kepada rekan Anda yang bekerja di bidang media monitoring.
