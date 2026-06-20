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

    # Seção de auto povoamento de categorias para as transações mais comuns, 
    # garantindo que o sistema já tenha uma base de regras para classificar as transações mais frequentes. 
    # Isso é especialmente útil para novos usuários que ainda não definiram suas próprias regras.   
    cursor.execute("SELECT count(*) FROM rules")
    if cursor.fetchone()[0] == 0:
        regras_iniciais = [
            ("Lider", "Supermercado"), ("Panificadorae", "Alimentação Fora"), 
            ("Cachorrinhola", "Alimentação Fora"), ("Espeto do Cheff", "Alimentação Fora"),
            ("Smash Burguers", "Alimentação Fora"), ("Haru", "Alimentação Fora"),
            ("Jeronimo'S", "Alimentação Fora"), ("Aliexpress", "Compras Online"),
            ("Alipay", "Compras Online"), ("Mercadolivre", "Compras Online"),
            ("Lasa", "Vestuário e Beleza"), ("Zerezes", "Vestuário e Beleza"),
            ("Sephora", "Vestuário e Beleza")
        ]
        cursor.executemany("INSERT OR IGNORE INTO rules (keyword, category) VALUES (?, ?)", regras_iniciais)

    conn.commit()
    conn.close()


def get_summary_table():
    conn = sqlite3.connect('finance.db')
    # Carrega dados
    df = pd.read_sql_query("SELECT date, category, amount FROM transactions", conn)
    conn.close()
    
    if df.empty:
        return None

    # Força a conversão para garantir que o .dt funcione
    df['date'] = pd.to_datetime(df['date'])
    df['mes'] = df['date'].dt.to_period('M').astype(str)
    
    # Cria o pivot table
    pivot = pd.pivot_table(
        df, 
        values='amount', 
        index='category', 
        columns='mes', 
        aggfunc='sum', 
        fill_value=0,
        margins=True, 
        margins_name='Total'
    )
    return pivot