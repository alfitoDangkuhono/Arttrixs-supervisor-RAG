"""
Chunking teks panjang menjadi bagian-bagian kecil
dengan overlap, agar cocok untuk embedding & retrieval.
"""

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP)->list[str]:
    """
    Memecah teks menjadi list of chunk berbasis jumlah kata.
    Args: 
        text: teks summber.
        chunk_size: jumlah kata per chunk.
        overlap: jumlah kata yang tumpang tindih antar chunk (membantu menajag konteks tidak terputus).

    Returns:
        List string, masing-masing chunk.
    """

    if not text:
        return []
    words = text.split()
    if len(words) <= chunk_size:
        return[text]
    chunk = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk.append(" ".join(words[start:end]))
        if end >= len(words):
            break
        start = end - overlap
    return chunk