import sqlite3

def classificar_transacao(titulo):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Busca todas as regras cadastradas
    try:
        cursor.execute("SELECT keyword, category FROM rules")
        regras = cursor.fetchall()
    except sqlite3.OperationalError:
        # Caso a tabela rules ainda não exista, retorna 'Outros'
        conn.close()
        return 'Outros'
    
    for keyword, category in regras:
        if keyword.lower() in titulo.lower():
            conn.close()
            return category
            
    conn.close()
    return 'Outros'

def reclassificar_todas_transacoes():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Pega todas as transações
    cursor.execute("SELECT id, title FROM transactions")
    transacoes = cursor.fetchall()
    
    # Pega todas as regras atuais
    cursor.execute("SELECT keyword, category FROM rules")
    regras = cursor.fetchall()
    
    for t_id, title in transacoes:
        nova_categoria = 'Outros'
        # Aplica a regra (a primeira que der match ganha)
        for keyword, category in regras:
            if keyword.lower() in title.lower():
                nova_categoria = category
                break
        
        # Atualiza o banco
        cursor.execute("UPDATE transactions SET category = ? WHERE id = ?", (nova_categoria, t_id))
    
    conn.commit()
    conn.close()

def adicionar_regra(keyword, category):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    try:
        # Usamos REPLACE para evitar erros caso a keyword já exista
        cursor.execute("INSERT OR REPLACE INTO rules (keyword, category) VALUES (?, ?)", (keyword, category))
        conn.commit()
    except Exception as e:
        print(f"Erro ao salvar regra: {e}")
    finally:
        conn.close()