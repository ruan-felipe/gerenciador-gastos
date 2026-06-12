import sqlite3

def classificar_transacao(titulo):
    """
    Analisa um título de transação e retorna a categoria correspondente.
    Se nenhuma regra for encontrada, retorna 'Outros'.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Tenta buscar as regras de classificação no banco
    try:
        cursor.execute("SELECT keyword, category FROM rules")
        regras = cursor.fetchall()
    except sqlite3.OperationalError:
        # Se a tabela não existir, encerra a conexão e retorna a categoria padrão
        conn.close()
        return 'Outros'
    
    # Compara o título da transação com todas as palavras-chave cadastradas.
    # O uso de .lower() garante que a busca seja case-insensitive (indiferente a maiúsculas/minúsculas)
    for keyword, category in regras:
        if keyword.lower() in titulo.lower():
            conn.close()
            return category
            
    conn.close()
    return 'Outros'

def reclassificar_todas_transacoes():
    """
    Realiza o processamento em lote (batch processing) de todas as transações
    existentes, reaplicando as regras de classificação atuais.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Obtém todo o histórico e o conjunto atual de regras
    cursor.execute("SELECT id, title FROM transactions")
    transacoes = cursor.fetchall()
    
    cursor.execute("SELECT keyword, category FROM rules")
    regras = cursor.fetchall()
    
    # Itera sobre cada transação para aplicar a lógica de classificação
    for t_id, title in transacoes:
        nova_categoria = 'Outros'
        
        # A primeira regra que contiver a palavra-chave é a que define a categoria
        for keyword, category in regras:
            if keyword.lower() in title.lower():
                nova_categoria = category
                break
        
        # Atualiza o banco de dados com a categoria encontrada
        cursor.execute("UPDATE transactions SET category = ? WHERE id = ?", (nova_categoria, t_id))
    
    # Consolida as alterações no banco de dados (commit)
    conn.commit()
    conn.close()

def adicionar_regra(keyword, category):
    """
    Insere uma nova regra de classificação ou atualiza uma existente.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    try:
        # Usa INSERT OR REPLACE para garantir que não tenhamos duplicidade de palavras-chave
        # garantindo que o sistema sempre mantenha a regra mais recente.
        cursor.execute("INSERT OR REPLACE INTO rules (keyword, category) VALUES (?, ?)", (keyword, category))
        conn.commit()
    except Exception as e:
        # Loga erros de banco de dados no console para debug
        print(f"Erro ao salvar regra: {e}")
    finally:
        # Garante que a conexão seja fechada independentemente de sucesso ou falha
        conn.close()
