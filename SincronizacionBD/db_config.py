import subprocess
import json
import sqlite3
import os

# Configuración de Access (usando PowerShell como en app_stock.py)
PS_SCRIPT = r"C:\Pescara\IA\WebApp\query_helper.ps1"
PS_EXE = r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe"

# Configuración de SQLite
SYNC_DB_PATH = os.path.join(os.path.dirname(__file__), "sync.db")

def execute_access_query(sql):
    """Ejecutar query en Access usando PowerShell (igual que app_stock.py)"""
    try:
        result = subprocess.run(
            [PS_EXE, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", PS_SCRIPT, sql],
            capture_output=True,
            text=True,
            encoding='latin-1',
            errors='replace'
        )

        if result.returncode != 0:
            raise Exception(f"Fallo en PS 32-bit: {result.stderr.strip()}")

        out = result.stdout.strip()
        if not out:
            return [], []

        # Limpiar output como en app_stock.py
        if out.find("[") != -1:
            out = out[out.find("["):]

        data = json.loads(out)
        if not isinstance(data, list):
            data = [data]

        if len(data) > 0:
            columns = list(data[0].keys())
            return columns, data
        else:
            return [], []
    except Exception as e:
        raise e

def get_sqlite_connection():
    """Conectar a SQLite"""
    try:
        conn = sqlite3.connect(SYNC_DB_PATH)
        conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
        return conn
    except Exception as e:
        raise Exception(f"Error conectando a SQLite: {e}")

def execute_sqlite_query(sql, params=None, fetch=True):
    """Ejecutar query en SQLite"""
    conn = None
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        if fetch:
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            return columns, [dict(zip(columns, row)) for row in rows]
        else:
            conn.commit()
            return None, None
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()