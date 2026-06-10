import streamlit as st
import os
from src.database import init_db
from src.utils import importar_csv_nubank

# 1. Configuração Inicial da Página
st.set_page_config(page_title="Gerenciador Financeiro", layout="wide")

# Inicializa o banco de dados ao carregar a aplicação
init_db()

st.title("💰 Gerenciador de Gastos")

# 2. Interface de Upload
uploaded_file = st.file_uploader("Escolha o arquivo CSV do Nubank", type="csv")

if uploaded_file is not None:
    # Como o Streamlit trabalha com arquivos na memória, precisamos salvar temporariamente
    # ou passar o buffer para o pandas. Aqui salvamos para atender sua lógica:
    with open("temp_nubank.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # Chama a função que criamos em utils.py
        total_importado = importar_csv_nubank("temp_nubank.csv")
        st.success(f"Sucesso! {total_importado} transações importadas.")
        
        # Remove o arquivo temporário após o uso
        os.remove("temp_nubank.csv")
        
    except Exception as e:
        st.error(f"Erro ao importar arquivo: {e}")

# 3. Área de visualização (Futuro)
st.divider()
st.write("Aqui você visualizará seus relatórios e o motor de resíduo.")
