import sqlite3
import pandas as pd

def get_transactions():
    """
    Recupera todas as transações cadastradas no banco de dados.
    Retorna um DataFrame do Pandas ordenado pela data mais recente (DESC).
    """
    conn = sqlite3.connect('finance.db')
    query = "SELECT * FROM transactions ORDER BY date DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_connection():
    """
    Fornece uma conexão genérica com o banco de dados finance.db.
    Útil para operações que precisam de controle manual de cursores.
    """
    return sqlite3.connect('finance.db')

def init_db():
    """
    Configuração inicial do banco de dados (Schema).
    Cria as tabelas caso não existam, garantindo a integridade do sistema.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Criação da tabela de transações:
    # A constraint UNIQUE(date, title, amount) previne que você importe 
    # o mesmo arquivo CSV várias vezes e crie transações duplicadas.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, 
            title TEXT, 
            amount REAL, 
            source TEXT,
            category TEXT DEFAULT 'Outros', -- Armazena a categoria definida pelas regras
            UNIQUE(date, title, amount)
        )
    ''')
    
    # Criação da tabela de regras:
    # A coluna 'keyword' tem a constraint UNIQUE para evitar que uma 
    # palavra-chave seja registrada duas vezes com categorias diferentes.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()
