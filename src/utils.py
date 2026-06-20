import pandas as pd
import sqlite3
import re
from src.processor import classificar_transacao

def importar_csv_nubank(arquivo_processado, nome_original):
    """
    Função principal de ETL (Extract, Transform, Load).
    1. Valida o nome do arquivo.
    2. Limpa e normaliza os dados.
    3. Insere novas transações no SQLite de forma atômica e segura.
    """
    
    # 1. Validação de formato: Garante que o arquivo segue o padrão de nomenclatura (Regex)
    if not re.match(r"^Nubank_\d{4}-\d{2}-\d{2}\.csv$", nome_original, re.IGNORECASE):
        raise ValueError(f"O arquivo '{nome_original}' não segue o padrão 'Nubank_yyyy-mm-dd.csv'")
    
    # 2. Leitura e Limpeza (Processamento do DataFrame)
    df = pd.read_csv(arquivo_processado)
    
    # Verifica se o arquivo CSV possui as colunas necessárias para o processamento
    if not all(col in df.columns for col in ['date', 'title', 'amount']):
        raise ValueError("O CSV deve conter as colunas: date, title, amount")
        
    # Normalização monetária: Remove aspas, espaços e converte para float/numérico
    df['amount'] = df['amount'].astype(str).str.replace('"', '', regex=False).str.strip()
    df['amount'] = df['amount'].str.replace(',', '.', regex=False).str.replace(' ', '', regex=False)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Remove linhas onde o valor não foi convertido corretamente
    df = df.dropna(subset=['amount'])
    df['source'] = 'CSV_NUBANK'
    
    # 3. Persistência de Dados (Gerenciamento seguro de conexão)
    # O bloco 'with' garante que a conexão seja fechada automaticamente ao final
    # e que as transações sejam confirmadas (commit) de forma segura.
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        novos_dados = 0
        
        for _, row in df.iterrows():
            # Verificação de duplicidade: Evita duplicar registros já importados no banco
            cursor.execute('''
                SELECT 1 FROM transactions 
                WHERE date = ? AND title = ? AND amount = ?
            ''', (row['date'], row['title'], row['amount']))
            
            # Se não encontrou o registro (None), prossegue com a inserção
            if cursor.fetchone() is None:
                # Classificação automática integrada no ato da importação
                categoria = classificar_transacao(row['title'])
                
                cursor.execute('''
                    INSERT INTO transactions (date, title, amount, source, category)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['date'], row['title'], row['amount'], row['source'], categoria))
                
                novos_dados += 1
                
    return novos_dados