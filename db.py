from dotenv import load_dotenv
import os
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from typing import Optional

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DBNAME = os.getenv("DB_NAME")

_pool: Optional[SimpleConnectionPool] = None

def init_db(minconn: int = 1, maxconn: int = 5):
    global _pool
    if _pool is not None:
        return
    _pool = SimpleConnectionPool(
        minconn,
        maxconn,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
    )

@contextmanager
def get_conn():
    """
    使用示例：
    with get_conn() as conn:
        cur = conn.cursor()
        ...
    """
    if _pool is None:
        init_db()
    assert _pool is not None, "_pool should be initialized before getting connection"
    conn = _pool.getconn()
    try:
        yield conn
    finally:
        _pool.putconn(conn)