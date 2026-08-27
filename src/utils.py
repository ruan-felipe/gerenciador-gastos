from ofxtools import OFXTree
import pandas as pd
import sqlite3
import re
from src.processor import classificar_transacao

def importar_ofx(arquivo_enviado):
    """
    Lê o arquivo OFX do Nubank de forma limpa, extrai as transações,
    aplica a categorização automática via regras e salva no SQLite.
    """
    # Lê o conteúdo do arquivo enviado pelo Streamlit (bytes ou string)
    if hasattr(arquivo_enviado, "read"):
        conteudo_bytes = arquivo_enviado.read()
        try:
            conteudo = conteudo_bytes.decode('utf-8')
        except UnicodeDecodeError:
            conteudo = conteudo_bytes.decode('latin-1')
    else:
        with open(arquivo_enviado, 'r', encoding='utf-8', errors='ignore') as f:
            conteudo = f.read()

    transacoes = []
    
    # Divide o arquivo cru por cada bloco de transação (<STMTTRN>)
    blocos = conteudo.split('<STMTTRN>')
    
    for bloco in blocos[1:]:
        try:
            # Regex robustas para capturar os dados ignorando fuso horário e tags fechadas
            match_data = re.search(r'<DTPOSTED>(\d{8})', bloco)
            match_valor = re.search(r'<TRNAMT>(-?\d+\.?\d*)', bloco)
            match_memo = re.search(r'<MEMO>(.*?)(?:</MEMO>|\r?\n|<|$)', bloco)
            
            if match_data and match_valor:
                # Trata a data (AAAAMMDD)
                data_str = match_data.group(1)[:8]
                data = pd.to_datetime(data_str, format='%Y%m%d').strftime('%Y-%m-%d')
                
                # Trata o valor
                valor = float(match_valor.group(1)) * -1
                
                # Trata a descrição (title)
                titulo = match_memo.group(1).strip() if match_memo else "Sem descrição"
                titulo = re.sub(r'<.*?>', '', titulo) # Remove tags residuais se houverem
                
                transacoes.append({
                    'date': data,
                    'title': titulo,
                    'amount': valor,
                    'source': 'OFX_NUBANK'
                })
        except Exception:
            continue

    if not transacoes:
        return 0

    df = pd.DataFrame(transacoes)
    
    # Inserção no banco de dados SQLite com aplicação de regras e blindagem contra duplicadas
    novos_dados = 0
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute('''
                SELECT 1 FROM transactions 
                WHERE date = ? AND title = ? AND amount = ?
            ''', (row['date'], row['title'], row['amount']))
            
            if cursor.fetchone() is None:
                # 1. AQUI ESTÁ A CORREÇÃO: Aplica a mesma regra inteligente do CSV
                categoria = classificar_transacao(row['title'])
                
                # 2. Insere no banco com a categoria já mapeada pelas suas regras
                cursor.execute('''
                    INSERT INTO transactions (date, title, amount, source, category) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['date'], row['title'], row['amount'], row['source'], categoria))
                novos_dados += 1
        conn.commit()
        
    return novos_dados
    
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