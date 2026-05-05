import os
import psycopg2
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv

load_dotenv()

def get_db_config():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        parsed = urlparse(database_url)
        return {
            "host": parsed.hostname,
            "port": parsed.port or 5432,
            "user": unquote(parsed.username or ""),
            "password": unquote(parsed.password or ""),
            "database": (parsed.path or "").lstrip("/"),
        }
    return None

config = get_db_config()
if config:
    conn = psycopg2.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        sslmode="require"
    )
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'gn_genomic_dataset'")
    for row in cur.fetchall():
        print(row[0])
    cur.close()
    conn.close()
else:
    print("No DATABASE_URL found")
