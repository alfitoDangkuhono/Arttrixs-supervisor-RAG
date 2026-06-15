-- ============================================
-- Schema untuk RAG Supervisor (PostgreSQL + pgvector)
-- Jalankan sekali via scripts/init_db.py
-- atau: psql -d ragdb -f db/schema.sql
-- ============================================
 
CREATE EXTENSION IF NOT EXISTS vector;
 
-- Tabel utama: menyimpan chunk teks + embedding + metadata
CREATE TABLE IF NOT EXISTS rag_documents (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    embedding VECTOR(384),          -- sesuaikan dengan EMBEDDING_DIM di config
    source_url TEXT,
    title TEXT,
    chunk_index INT,
    total_chunks INT,
    query_topic TEXT,
    scraped_at TIMESTAMP
);
 
-- Index untuk similarity search (cosine distance)
CREATE INDEX IF NOT EXISTS rag_documents_embedding_idx
    ON rag_documents USING hnsw (embedding vector_cosine_ops);
 
-- Tabel untuk tracking URL yang sudah pernah diproses (hindari duplikat)
CREATE TABLE IF NOT EXISTS processed_urls (
    url TEXT PRIMARY KEY,
    processed_at TIMESTAMP DEFAULT NOW()
);