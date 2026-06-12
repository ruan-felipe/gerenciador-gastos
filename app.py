import streamlit as st
import os
from src.database import init_db, get_transactions # Adicione o get_transactions
from src.utils import importar_csv_nubank
from src.processor import classificar_transacao, reclassificar_todas_transacoes, adicionar_regra


# 1. Configuração Inicial da Página
st.set_page_config(page_title="Gerenciador Financeiro", layout="wide")

# Inicializa o banco de dados ao carregar a aplicação
init_db()

st.title("💰 Gerenciador de Gastos")

# 2. Interface de Upload
uploaded_files = st.file_uploader("Escolha os arquivos CSV do Nubank", type="csv", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        nome_original = uploaded_file.name
        try:
            count = importar_csv_nubank(uploaded_file, nome_original)
            if count > 0:
                st.success(f"Arquivo {nome_original}: {count} novas transações adicionadas.")
            else:
                st.info(f"Arquivo {nome_original}: Nenhuma transação nova (ou tudo já importado).")
        except ValueError as e:
            st.error(f"Erro no arquivo {nome_original}: {str(e)}")

# 3. Área de visualização (Futuro)
st.divider()
st.subheader("📊 Transações Recentes")

# Busca os dados do banco
df_transacoes = get_transactions()

if not df_transacoes.empty:
    # Exibe a tabela no Streamlit
    st.dataframe(df_transacoes, use_container_width=True)
else:
    st.info("Nenhuma transação encontrada no banco de dados.")

# 4. painel administrativo para regras de classificação (Futuro)

with st.expander("⚙️ Gerenciar Categorias"):
    # Entradas de dados
    col1, col2 = st.columns(2)
    with col1:
        nova_keyword = st.text_input("Palavra-chave (ex: Amazon)")
    with col2:
        nova_categoria = st.text_input("Categoria (ex: Lazer)")
    
    # Botão para salvar regra
    if st.button("Salvar Regra"):
        if nova_keyword and nova_categoria:
            # Chama a função que criamos no processor.py
            adicionar_regra(nova_keyword, nova_categoria)
            st.success(f"Regra '{nova_keyword}' -> '{nova_categoria}' salva!")
        else:
            st.warning("Preencha todos os campos antes de salvar.")

    st.divider()

    # Botão de reclassificação
    st.write("Deseja atualizar transações antigas com as novas regras?")
    if st.button("Aplicar nova regra em transações antigas"):
        with st.spinner("Reclassificando..."):
            reclassificar_todas_transacoes()
            st.success("Todas as transações foram reclassificadas!")
            st.rerun() # Recarrega para mostrar as novas categorias na tabela