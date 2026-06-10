import pandas as pd
import sqlite3

def importar_csv_nubank(caminho_arquivo):
    """
    Lê o CSV do Nubank (date, title, amount), limpa os dados e insere no SQLite.
    """
    # Lê o arquivo CSV
    # O Nubank costuma usar separador de vírgula ou ponto e vírgula, 
    # se der erro, ajuste o parâmetro 'sep' (ex: sep=';')
    df = pd.read_csv(caminho_arquivo)
    
    # Valida se as colunas estão no formato esperado
    if not all(col in df.columns for col in ['date', 'title', 'amount']):
        raise ValueError("O CSV deve conter as colunas: date, title, amount")
    
    # Limpeza dos dados:
    # 1. Converte a coluna 'amount' para float (caso venha com R$ ou formato texto)
    # Remove 'R$', espaços e substitui vírgula por ponto
    df['amount'] = df['amount'].replace({r'R\$': '', r'\.': '', ',': '.'}, regex=True).astype(float)
    
    # 2. Adiciona a origem dos dados para controle interno
    df['source'] = 'CSV_NUBANK'
    
    # 3. Garante que os nomes das colunas batam com o banco (ajuste se necessário)
    df = df.rename(columns={'date': 'date', 'title': 'description', 'amount': 'amount'})
    
    # Conecta ao banco e salva os dados
    conn = sqlite3.connect('finance.db')
    df.to_sql('transactions', conn, if_exists='append', index=False)
    conn.close()
    
    return len(df)
