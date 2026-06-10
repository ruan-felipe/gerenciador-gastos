# Gerenciador de Gastos

Uma aplicação de controle financeiro inteligente, desenvolvida para resolver a ambiguidade de gastos em estabelecimentos híbridos. Diferente de um simples rastreador de despesas, este sistema realiza a **conciliação automática** entre o seu extrato bancário (Nubank) e seus lançamentos manuais diários, utilizando uma lógica de cálculo residual para garantir precisão máxima.

## 🚀 O Problema
Gerenciar gastos em locais como supermercados é difícil porque eles vendem de tudo (comida, remédios, pets, vestuário). O sistema tradicional de apenas importar o CSV mascara essas variações. Este projeto permite manter o controle diário e, ao final do mês, cruzar dados com o extrato bancário, permitindo a divisão inteligente (splits) e o cálculo automático do valor residual.

## ⚙️ Funcionalidades
*   **Conciliação Dual-Source:** Integra lançamentos manuais com a importação de CSV do Nubank.
*   **Lógica de Resíduo (Smart Split):** Deduz gastos específicos de uma fatura maior, atribuindo o restante automaticamente à categoria principal.
*   **Projeção Financeira:** Calcula o fechamento da fatura baseado no padrão de consumo.
*   **Dashboard Interativo:** Visualização de gastos mensais e por categoria.

## 🛠️ Stack Tecnológico
*   **Linguagem:** Python
*   **Interface:** Streamlit
*   **Manipulação de Dados:** Pandas
*   **Visualização:** Plotly
*   **Banco de Dados:** SQLite

## 🏗️ Estrutura
O projeto é modularizado em:
1. **Ingestão:** Processamento e limpeza de dados (ETL).
2. **Motor de Regras:** Lógica de conciliação e cálculo residual.
3. **Interface (UI):** Dashboard interativo para gestão.

---
*Desenvolvido como projeto de Engenharia de Computação.*
