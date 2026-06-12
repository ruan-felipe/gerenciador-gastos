import streamlit as st
import os
# Importações de módulos locais:
# database.py: Gerencia a estrutura do banco e conexão
# utils.py: Contém lógica de manipulação de arquivos (CSV)
# processor.py: Contém regras de negócio e classificação
from src.database import init_db, get_transactions
from src.utils import importar_csv_nubank
from src.processor import classificar_transacao, reclassificar_todas_transacoes, adicionar_regra

# 1. Configuração Inicial da Página
# Define o layout da aplicação como 'wide' para ocupar toda a largura da tela
st.set_page_config(page_title="Gerenciador Financeiro", layout="wide")

# Garante que as tabelas necessárias existam no arquivo finance.db
init_db()

st.title("💰 Gerenciador de Gastos")

# 2. Interface de Upload
# Componente para carregar arquivos. 'accept_multiple_files' permite subir vários extratos de uma vez
uploaded_files = st.file_uploader("Escolha os arquivos CSV do Nubank", type="csv", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        nome_original = uploaded_file.name
        try:
            # Chama a função de importação que lê o CSV e insere no banco
            count = importar_csv_nubank(uploaded_file, nome_original)
            if count > 0:
                st.success(f"Arquivo {nome_original}: {count} novas transações adicionadas.")
            else:
                st.info(f"Arquivo {nome_original}: Nenhuma transação nova (ou tudo já importado).")
        except ValueError as e:
            # Tratamento de erro caso o formato do CSV seja inválido
            st.error(f"Erro no arquivo {nome_original}: {str(e)}")

# 3. Área de Visualização
st.divider()
st.subheader("📊 Transações Recentes")

# Busca os dados atuais do banco de dados (retorna um DataFrame do Pandas)
df_transacoes = get_transactions()

if not df_transacoes.empty:
    # Renderiza a tabela de forma interativa na interface
    st.dataframe(df_transacoes, use_container_width=True)
else:
    st.info("Nenhuma transação encontrada no banco de dados.")

# 4. Painel Administrativo
# O 'expander' mantém a interface limpa, ocultando controles avançados
with st.expander("⚙️ Gerenciar Categorias"):
    # Organiza os inputs de texto lado a lado
    col1, col2 = st.columns(2)
    with col1:
        nova_keyword = st.text_input("Palavra-chave (ex: Amazon)")
    with col2:
        nova_categoria = st.text_input("Categoria (ex: Lazer)")
    
    # Botão para persistir uma nova regra de classificação no banco
    if st.button("Salvar Regra"):
        if nova_keyword and nova_categoria:
            adicionar_regra(nova_keyword, nova_categoria)
            st.success(f"Regra '{nova_keyword}' -> '{nova_categoria}' salva!")
        else:
            st.warning("Preencha todos os campos antes de salvar.")

    st.divider()

    # Funcionalidade de atualização em lote (Batch update)
    # Útil quando o usuário cadastra uma nova regra e quer aplicá-la ao histórico antigo
    st.write("Deseja atualizar transações antigas com as novas regras?")
    if st.button("Aplicar nova regra em transações antigas"):
        with st.spinner("Reclassificando..."):
            reclassificar_todas_transacoes()
            st.success("Todas as transações foram reclassificadas!")
            # Recarrega a página para atualizar a tabela exibida com as novas categorias
            st.rerun()
