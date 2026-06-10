import sqlite3

def get_connection():
    return sqlite3.connect('finance.db')

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Criação da tabela de transações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            title TEXT,
            amount REAL,
            category TEXT,
            source TEXT
        )
    ''')
    conn.commit()
    conn.close()
