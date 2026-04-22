import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "clinica_db",
    "user": "postgres",
    "password": "espe"
}

def obtener_conexion():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)