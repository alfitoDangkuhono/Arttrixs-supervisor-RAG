"""
Generate embedding vector dari teks menggunakan
sentence-transformers (model berjalan lokal, tidak perlu API KEY)
"""

from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

_model = None

def get_model():
    """
    Lazy-load model agar hanya dimuat sekali(model cukup besar).
    """

    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
        return _model
    
def embed_texts(texts: list[str]):

    """
    Generate embedding untuk list teks.
    Return: 
        numpy.ndarray dengan shape (len(texts), EMBEDDING_DIM)
    """
    model = get_model()
    return model.encode(texts, show_progress_bar=False)