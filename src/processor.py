import sqlite3
import pandas as pd

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
    
    # Compara o título da transação com todas as palavras-chave cadastradas (case-insensitive)
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
        cursor.execute("INSERT OR REPLACE INTO rules (keyword, category) VALUES (?, ?)", (keyword, category))
        conn.commit()
    except Exception as e:
        print(f"Erro ao salvar regra: {e}")
    finally:
        conn.close()

def calcular_fatura_competencia(df_transacoes, dia_vencimento):
    """
    Calcula a competência das transações de acordo com o ciclo da fatura.

    Regras:
    - O vencimento deve estar entre os dias 1 e 27.
    - O fechamento ocorre 8 dias corridos antes do vencimento.
    - O próprio dia do fechamento pertence à fatura que está fechando.
    - Compras após o fechamento pertencem à próxima fatura.
    - A competência corresponde ao mês anterior ao vencimento da fatura.

    Exemplo com vencimento no dia 07:

        29/04 -> fechamento -> fatura 07/05 -> competência 2026-04
        30/04 -> após fechamento -> fatura 07/06 -> competência 2026-05

        30/05 -> fechamento -> fatura 07/06 -> competência 2026-05
        31/05 -> após fechamento -> fatura 07/07 -> competência 2026-06
    """

    if df_transacoes.empty:
        return df_transacoes

    if not 1 <= dia_vencimento <= 27:
        raise ValueError(
            "O dia de vencimento deve estar entre 1 e 27."
        )

    df = df_transacoes.copy()
    df["date"] = pd.to_datetime(df["date"])

    def definir_fatura(data):
        # Primeiro consideramos o vencimento do mês seguinte
        # ao mês da compra.
        vencimento = (
            pd.Timestamp(
                year=data.year,
                month=data.month,
                day=1
            )
            + pd.DateOffset(months=1)
        )

        vencimento = vencimento.replace(day=dia_vencimento)

        # O fechamento ocorre 8 dias corridos antes.
        fechamento = vencimento - pd.Timedelta(days=8)

        # Se a compra ocorreu depois do fechamento,
        # ela pertence à fatura seguinte.
        if data > fechamento:
            vencimento_fatura = vencimento + pd.DateOffset(months=1)
        else:
            vencimento_fatura = vencimento

        # A competência é o mês anterior ao vencimento.
        competencia = (
            vencimento_fatura - pd.DateOffset(months=1)
        )

        return competencia.strftime("%Y-%m")

    df["fatura_ref"] = df["date"].apply(definir_fatura)

    return df

def gerar_resumo_categorias(df_transacoes):
    """
    Gera a tabela dinâmica (pivot table) agrupando os gastos por categoria 
    e competência da fatura (fatura_ref). Exclui pagamentos recebidos e mantém estornos.
    """
    if df_transacoes.empty:
        return pd.DataFrame()

    # Filtra para excluir pagamentos da fatura, mantendo estornos (negativos)
    df_gastos = df_transacoes[
        ~df_transacoes['title'].str.contains('Pagamento recebido', case=False, na=False)
    ].copy()

    # Cria a tabela dinâmica (Pivot Table)
    pivot = pd.pivot_table(
        df_gastos, 
        values='amount', 
        index='category', 
        columns='fatura_ref', 
        aggfunc='sum', 
        fill_value=0, 
        margins=True, 
        margins_name='Total'
    ).drop(columns=['Total'], errors='ignore')
    
    return pivot