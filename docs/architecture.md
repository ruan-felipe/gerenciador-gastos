# Arquitetura do Sistema

## 1. Visão Geral
O Conciliador Financeiro foi desenhado com base em uma arquitetura modular, visando a separação de responsabilidades (Separation of Concerns). Esta abordagem facilita a manutenção, testes unitários e a eventual expansão para outras plataformas (ex: integração via API ou bot).

## 2. Stack Tecnológico
*   **Linguagem:** Python 3.x
*   **Interface (UI/UX):** Streamlit (Framework para aplicações de dados)
*   **Manipulação de Dados (ETL):** Pandas (DataFrames para processamento em memória)
*   **Persistência de Dados:** SQLite (Banco de dados relacional leve, ideal para aplicações desktop e pequenas ferramentas web)

## 3. Design Pattern (Modularização)
A estrutura segue um padrão de organização lógica inspirado no modelo MVC (Model-View-Controller), adaptado para o escopo do projeto:

*   **Camada de Apresentação (`app.py`):** Responsável por renderizar a interface, capturar eventos de input (upload de arquivos) e exibir os resultados. Não contém regras de negócio.
*   **Camada de Regra de Negócio (`src/processor.py`):** O "Cérebro do sistema". Processa as conciliações, calcula o resíduo e aplica as regras de *split*.
*   **Camada de Acesso a Dados (`src/database.py` e `src/utils.py`):** Gerencia a persistência (SQL) e a ingestão de dados brutos (CSV).

## 4. Estrutura de Diretórios
```text
/
├── app.py              # Ponto de entrada (UI)
├── finance.db          # Base de dados (SQLite)
├── src/                # Código fonte (lógica e backend)
│   ├── database.py     # Definição do Schema e Conexões
│   ├── utils.py        # ETL e Ingestão de CSVs
│   └── processor.py    # Algoritmo de Conciliação e Splits
└── docs/               # Documentação técnica
