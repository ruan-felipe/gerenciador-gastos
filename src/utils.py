import pandas as pd
import sqlite3
import os

def importar_csv_nubank(caminho_arquivo):
    """
    Lê o CSV do Nubank (date, title, amount), valida o nome do arquivo 
    e insere no SQLite.
    """
    # 1. Validação do nome do arquivo
    nome_arquivo = os.path.basename(caminho_arquivo)
    
    if not nome_arquivo.startswith("Nubank_"):
        raise ValueError("Erro: O arquivo selecionado não segue o padrão 'Nubank_yyyy-mm-dd.csv'")
    
    # Opcional: Extrair a data do nome do arquivo para usar se precisar
    data_do_arquivo = nome_arquivo.replace("Nubank_", "").replace(".csv", "")
    print(f"Processando arquivo referente a: {data_do_arquivo}")

    # 2. Lê o arquivo CSV
    df = pd.read_csv(caminho_arquivo)
    
    # 3. Validação das colunas
    if not all(col in df.columns for col in ['date', 'title', 'amount']):
        raise ValueError("O CSV deve conter as colunas: date, title, amount")
    
    # 4. Limpeza
    df['amount'] = df['amount'].replace({r'R\$': '', r'\.': '', ',': '.'}, regex=True).astype(float)
    
    # 5. Seleção e origem
    df = df[['date', 'title', 'amount']]
    df['source'] = 'CSV_NUBANK'
    
    # 6. Salvando no banco
    conn = sqlite3.connect('finance.db')
    df.to_sql('transactions', conn, if_exists='append', index=False)
    conn.close()
    
    return len(df)
