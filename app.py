import streamlit as st
import pandas as pd
from src.database import init_db, get_transactions
from src.utils import importar_csv_nubank
from src.processor import reclassificar_todas_transacoes, adicionar_regra

# 1. Configuração Inicial da Página
st.set_page_config(page_title="Gerenciador Financeiro", layout="wide")
init_db()

st.title("💰 Gerenciador de Gastos")

# Sidebar para configuração dinâmica
st.sidebar.subheader("⚙️ Configurações")
dia_fechamento = st.sidebar.number_input("Dia de fechamento da fatura", min_value=1, max_value=31, value=7)

# 2. Interface de Upload
uploaded_files = st.file_uploader("Escolha os arquivos CSV do Nubank", type="csv", accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            count = importar_csv_nubank(uploaded_file, uploaded_file.name)
            if count > 0: st.success(f"{uploaded_file.name}: {count} novas transações.")
        except ValueError as e:
            st.error(f"Erro no arquivo {uploaded_file.name}: {str(e)}")

st.divider()

# 3. Processamento e Visualização
df_transacoes = get_transactions()

if not df_transacoes.empty:
    df_transacoes['date'] = pd.to_datetime(df_transacoes['date'])

    # Lógica de Fatura Dinâmica
    def definir_fatura(data, dia_corte):
        # Se o dia é <= corte, pertence ao mês atual; senão, próximo mês
        if data.day <= dia_corte:
            return data.to_period('M')
        else:
            return (data + pd.offsets.MonthEnd(0)).to_period('M')

    df_transacoes['fatura_ref'] = df_transacoes['date'].apply(lambda x: definir_fatura(x, dia_fechamento)).astype(str)

    # Filtro para Resumo: Exclui pagamentos, mantém estornos (negativos)
    df_gastos = df_transacoes[~df_transacoes['title'].str.contains('Pagamento recebido', case=False, na=False)].copy()

    # --- Resumo (Pivot) ---
    st.subheader("📊 Resumo de Gastos (Consumo Líquido)")
    pivot = pd.pivot_table(
        df_gastos, values='amount', index='category', columns='fatura_ref', 
        aggfunc='sum', fill_value=0, margins=True, margins_name='Total'
    ).drop(columns=['Total'], errors='ignore')
    
    st.dataframe(pivot.style.format("{:.2f}"), use_container_width=True)

    # --- Valor Total da Fatura ---
    total_fatura = df_gastos['amount'].sum()
    st.metric(label="Valor Líquido Estimado (Total de Gastos + Estornos)", value=f"R$ {total_fatura:.2f}")

    # --- Transações Recentes ---
    st.subheader("📊 Transações Recentes")
    st.dataframe(df_transacoes.sort_values(by='date', ascending=False), use_container_width=True)

else:
    st.info("Nenhuma transação encontrada. Por favor, faça o upload de um extrato.")

# 4. Painel Administrativo
with st.expander("⚙️ Gerenciar Categorias"):
    col1, col2 = st.columns(2)
    with col1: nova_keyword = st.text_input("Palavra-chave (ex: Amazon)")
    with col2: nova_categoria = st.text_input("Categoria (ex: Lazer)")
    
    if st.button("Salvar Regra e Atualizar"):
        if nova_keyword and nova_categoria:
            adicionar_regra(nova_keyword, nova_categoria)
            reclassificar_todas_transacoes()
            st.rerun()
        else:
            st.warning("Preencha todos os campos.")