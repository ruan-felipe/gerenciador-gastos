import pandas as pd
import sqlite3
import os
import re
from src.processor import classificar_transacao

def importar_csv_nubank(arquivo_processado, nome_original):
    # 1. Validação do nome
    if not re.match(r"^Nubank_\d{4}-\d{2}-\d{2}\.csv$", nome_original, re.IGNORECASE):
        raise ValueError(f"O arquivo '{nome_original}' não segue o padrão 'Nubank_yyyy-mm-dd.csv'")
    
    # 2. Leitura e Limpeza
    df = pd.read_csv(arquivo_processado)
    
    # Verifica colunas necessárias
    if not all(col in df.columns for col in ['date', 'title', 'amount']):
        raise ValueError("O CSV deve conter as colunas: date, title, amount")
        
    df['amount'] = df['amount'].astype(str).str.replace('"', '', regex=False).str.strip()
    df['amount'] = df['amount'].str.replace(',', '.', regex=False).str.replace(' ', '', regex=False)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['amount'])
    df['source'] = 'CSV_NUBANK'
    
    # 3. Conexão e Filtragem de Duplicatas linha a linha
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    novos_dados = 0
    # Iteramos linha a linha para verificar unicidade no banco

    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    novos_dados = 0
    
    # Este é o loop que você perguntou
    for _, row in df.iterrows():
        # Verifica duplicatas (já existe?)
        cursor.execute('''
            SELECT 1 FROM transactions 
            WHERE date = ? AND title = ? AND amount = ?
        ''', (row['date'], row['title'], row['amount']))
        
        # Se não existe no banco, prosseguimos
        if cursor.fetchone() is None:
            # 1. Classifica a transação usando a nova função
            categoria = classificar_transacao(row['title'])
            
            # 2. Insere no banco com a categoria encontrada
            cursor.execute('''
                INSERT INTO transactions (date, title, amount, source, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['date'], row['title'], row['amount'], row['source'], categoria))
            
            novos_dados += 1
            
    conn.commit()
    conn.close()
    
    return novos_dados