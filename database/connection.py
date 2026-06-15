"""
Helper koneksi PostgreSQL.
"""
import psycopg2
from config.settings import DB_CONFIG

def get_connection():
    """Membuat koneksi baru ke PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)