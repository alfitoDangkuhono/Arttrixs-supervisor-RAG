# RAG Supervisor

Pipeline otomatis yang mencari informasi terbaru dari internet (via Tavily
Search API), mengubahnya menjadi embedding, dan menyimpannya ke PostgreSQL
(pgvector) untuk digunakan sebagai knowledge base RAG. Project ini sekarang
juga dilengkapi dengan API FastAPI sehingga hasil query bisa diakses dari
hosting atau aplikasi lain.

## Struktur Project

```
rag-supervisor/
├── app.py          API FastAPI untuk query RAG dan health check
├── config/         konfigurasi (.env, topik, model embedding, dll)
├── database/       schema SQL & koneksi Postgres
├── collectors/     pencarian (Tavily) & fetch konten web
├── processing/     chunking & embedding teks
├── supervisor/     pipeline utama: search -> chunk -> embed -> simpan
├── scheduler/      menjalankan supervisor secara berkala
├── rag/            retriever untuk similarity search
└── scripts/        utility (init database)
```

## Setup

1. Buat virtual environment & install dependency

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Pastikan PostgreSQL sudah terinstall extension `pgvector`.

3. Buat file `.env` (atau salin dari `.env.example` bila ada) dan isi:
   - `TAVILY_API_KEY` (daftar gratis di tavily.com)
   - kredensial database (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, dll)
   - `EMBEDDING_MODEL` (opsional, default: `all-MiniLM-L6-v2`)
   - `EMBEDDING_DIM` (opsional, default: 384)
   - `MAX_RESULTS_PER_TOPIC` (opsional)

   ```bash
   copy .env.example .env
   ```

4. Inisialisasi database (membuat extension, tabel, index):

   ```bash
   python scripts/init_db.py
   ```

## Konfigurasi Topik

Edit `config/settings.py`, ubah list `TOPICS` sesuai topik yang ingin
dipantau supervisor:

```python
TOPICS = [
    "perkembangan AI lokal terbaru",
    "framework RAG terbaru",
]
```

## Menjalankan

### 1. Jalankan pipeline supervisor

```bash
python -m supervisor.pipeline
```

### 2. Jalankan API FastAPI untuk hosting

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

Setelah server berjalan, buka:

- http://localhost:8000/docs
- http://localhost:8000/health
- http://localhost:8000/api/search?query=framework%20RAG%20terbaru&top_k=5

### 3. Jalankan scheduler bawaan

```bash
python scheduler/scheduler.py
```

Akan jalan sekali saat start, lalu berulang setiap `SCHEDULE_INTERVAL_HOURS`
jam (default 1 jam, atur di `.env`).

### Berkala via cron (alternatif)

```bash
# tambahkan ke crontab -e, contoh tiap jam:
0 * * * * cd /path/to/rag-supervisor && /path/to/venv/bin/python -m supervisor.pipeline >> logs/supervisor.log 2>&1
```

## Menggunakan API

Endpoint utama:

```http
GET /api/search?query=framework RAG terbaru&top_k=5
```

Response contoh:

```json
{
  "query": "framework RAG terbaru",
  "top_k": 5,
  "count": 5,
  "context": "...",
  "results": [
    {
      "text": "...",
      "source_url": "https://example.com",
      "title": "...",
      "similarity": 0.91
    }
  ]
}
```

## Menggunakan untuk RAG (LLM lokal)

```python
from rag.retriever import build_context

context = build_context("apa itu RAG", top_k=5)

prompt = f"""Berdasarkan informasi berikut:

{context}

Jawab pertanyaan: apa itu RAG"""

# kirim prompt ke LLM lokal (Ollama, llama.cpp, dll)
```

Atau jalankan langsung dari terminal untuk uji coba:

```bash
python -m rag.retriever "apa itu RAG"
```

## Catatan

- Model embedding default: `all-MiniLM-L6-v2` (384 dimensi, ringan, jalan
  di CPU). Jika ganti model dengan dimensi berbeda, update juga
  `EMBEDDING_DIM` di `.env` dan `VECTOR(...)` di `database/schema.sql`.
- Deduplikasi URL disimpan di tabel `processed_urls` agar tidak
  diproses ulang.
- Free tier Tavily: ~1000 request/bulan — sesuaikan jumlah topik dan
  interval scheduler agar tidak melebihi kuota.