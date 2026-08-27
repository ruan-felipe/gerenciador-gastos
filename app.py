import streamlit as st
import pandas as pd
from src.database import init_db, get_transactions
from src.utils import importar_csv_nubank, importar_ofx
from src.processor import (
    calcular_fatura_competencia, 
    gerar_resumo_categorias, 
    reclassificar_todas_transacoes, 
    adicionar_regra
)

# 1. Configuração Inicial da Página
st.set_page_config(page_title="Gerenciador Financeiro", layout="wide")
init_db()

st.title("💰 Gerenciador de Gastos")

# Sidebar para configuração dinâmica
st.sidebar.subheader("⚙️ Configurações da Fatura")
dia_vencimento = st.sidebar.number_input(
    "Dia de Vencimento da Fatura", 
    min_value=1, 
    max_value=31, 
    value=7, 
    step=1,
    help="O fechamento é calculado automaticamente 7 dias antes do vencimento."
)

# 2. Interface de Upload
formato_arquivo = st.radio("Selecione o formato do arquivo:", ["CSV (Nubank)", "OFX (Padrão Bancário)"], horizontal=True)

uploaded_files = st.file_uploader(f"Escolha os arquivos {formato_arquivo}", type=["csv", "ofx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            # Lógica de roteamento baseada no formato selecionado
            if "CSV" in formato_arquivo:
                count = importar_csv_nubank(uploaded_file, uploaded_file.name)
            else:
                count = importar_ofx(uploaded_file)

            # Proteção contra valores nulos/inválidos
            if count is not None and count > 0: 
                st.success(f"{uploaded_file.name}: {count} novas transações adicionadas.")
            else:
                st.info(f"{uploaded_file.name}: Nenhuma transação nova encontrada ou arquivo já importado.")
                
        except Exception as e:
            st.error(f"Erro ao processar {uploaded_file.name}: {str(e)}")

st.divider()

# 3. Processamento e Visualização
df_raw = get_transactions()

if not df_raw.empty:
    # Delega o cálculo do ciclo de fatura para o processor.py
    df_transacoes = calcular_fatura_competencia(df_raw, dia_vencimento)

    # --- Resumo (Pivot Table) por Fatura de Competência (Delegação para o processor.py) ---
    st.subheader("📊 Resumo de Gastos por Fatura (Competência)")
    
    pivot_resumo = gerar_resumo_categorias(df_transacoes)
    
    if not pivot_resumo.empty:
        st.dataframe(pivot_resumo.style.format("{:.2f}"), use_container_width=True)
    else:
        st.info("Nenhum dado de despesa para exibir no resumo.")

    # --- Valor Total da Fatura (Excluindo pagamentos recebidos) ---
    df_gastos = df_transacoes[
        ~df_transacoes['title'].str.contains('Pagamento recebido', case=False, na=False)
    ]
    total_fatura = df_gastos['amount'].sum()
    st.metric(label="Valor Líquido Estimado da Fatura", value=f"R$ {total_fatura:.2f}")

    # --- Transações Recentes ---
    st.subheader("🔍 Transações Recentes")
    st.dataframe(df_transacoes.sort_values(by='date', ascending=False), use_container_width=True)

else:
    st.info("Nenhuma transação encontrada. Por favor, faça o upload de um extrato na barra lateral.")

# 4. Painel Administrativo de Regras
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