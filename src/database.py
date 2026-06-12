import sqlite3
import pandas as pd

def get_transactions():
    conn = sqlite3.connect('finance.db')
    query = "SELECT * FROM transactions ORDER BY date DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_connection():
    return sqlite3.connect('finance.db')

def init_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Tabela de transações (mantida)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, title TEXT, amount REAL, source TEXT,
            category TEXT DEFAULT 'Outros', -- Nova coluna para a classificação
            UNIQUE(date, title, amount)
        )
    ''')
    
    # Tabela de regras de classificação
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()