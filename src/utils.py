import pandas as pd
import sqlite3
import os
import re
from src.processor import classificar_transacao

def importar_csv_nubank(arquivo_processado, nome_original):
    """
    Função principal de ETL.
    1. Valida o nome do arquivo.
    2. Limpa e normaliza os dados (DataFrame).
    3. Insere apenas novas transações no SQLite (prevenindo duplicatas).
    """
    
    # 1. Validação de formato: Garante que o arquivo é um CSV do Nubank (Regex)
    # Isso evita erros de processar arquivos errados ou fora do padrão
    if not re.match(r"^Nubank_\d{4}-\d{2}-\d{2}\.csv$", nome_original, re.IGNORECASE):
        raise ValueError(f"O arquivo '{nome_original}' não segue o padrão 'Nubank_yyyy-mm-dd.csv'")
    
    # 2. Leitura e Limpeza (Processamento do DataFrame)
    df = pd.read_csv(arquivo_processado)
    
    # Validação de esquema: Verifica se as colunas obrigatórias existem
    if not all(col in df.columns for col in ['date', 'title', 'amount']):
        raise ValueError("O CSV deve conter as colunas: date, title, amount")
        
    # Normalização monetária: Remove caracteres indesejados e converte para float
    df['amount'] = df['amount'].astype(str).str.replace('"', '', regex=False).str.strip()
    df['amount'] = df['amount'].str.replace(',', '.', regex=False).str.replace(' ', '', regex=False)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Remove linhas inválidas onde o valor não foi convertido
    df = df.dropna(subset=['amount'])
    df['source'] = 'CSV_NUBANK'
    
    # 3. Persistência de Dados
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    novos_dados = 0
    
    # Iteração sobre cada linha para inserção controlada
    for _, row in df.iterrows():
        # Verificação de duplicidade: Evita duplicar registros já importados
        cursor.execute('''
            SELECT 1 FROM transactions 
            WHERE date = ? AND title = ? AND amount = ?
        ''', (row['date'], row['title'], row['amount']))
        
        # Se não encontrou o registro (fetchone é None), insere
        if cursor.fetchone() is None:
            # Integração com o módulo processor: Classifica automaticamente no ato da importação
            categoria = classificar_transacao(row['title'])
            
            cursor.execute('''
                INSERT INTO transactions (date, title, amount, source, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['date'], row['title'], row['amount'], row['source'], categoria))
            
            novos_dados += 1
            
    conn.commit()
    conn.close()
    
    return novos_dados
