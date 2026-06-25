# Arquitetura do Sistema

## 1. Visão Geral
O Conciliador Financeiro foi desenhado com base em uma arquitetura modular, visando a separação de responsabilidades (*Separation of Concerns*). Esta abordagem facilita a manutenção, a testabilidade unitária e a escalabilidade para novas fontes de dados bancários (CSV/OFX).

## 2. Stack Tecnológico
* **Linguagem:** Python 3.x
* **Interface (UI/UX):** Streamlit (Framework reativo para aplicações de dados)
* **Engenharia de Dados (ETL):** Pandas (DataFrames para processamento em memória e normalização)
* **Persistência:** SQLite (Banco de dados relacional com integridade referencial)
* **Parsers Bancários:** `ofxtools` (Para processamento de arquivos OFX)

## 3. Design Pattern (Modularização)
A estrutura segue um padrão de organização lógica inspirado no modelo MVC, adaptado para o escopo de um sistema de conciliação:

* **Camada de Apresentação (`app.py`):** Responsável por renderizar a interface, capturar eventos de input e exibir os resultados. Implementa a lógica de fatura dinâmica baseada no `dia_fechamento`.
* **Camada de Regra de Negócio (`src/processor.py`):** O "Cérebro do sistema". Processa as conciliações, calcula o resíduo (Smart Split) e aplica as regras de classificação (`reclassificar_todas_transacoes`).
* **Camada de Ingestão e ETL (`src/utils.py`):** Módulo crítico. Responsável pela normalização de fontes heterogêneas (CSV/OFX) para um schema unificado.
* **Camada de Acesso a Dados (`src/database.py`):** Gerencia a persistência (SQL), contendo as *constraints* de integridade (ex: `UNIQUE` em transações para evitar duplicidade).

## 4. Fluxo de Processamento de Dados (Pipeline)
1. **Ingestão:** O `utils.py` detecta a fonte (CSV ou OFX).
2. **Normalização:** O parser converte a estrutura do arquivo para um `DataFrame` padrão (Campos: `date`, `title`, `amount`).
3. **Consistência:** Verificação de duplicidade no banco (`UNIQUE`) antes da inserção.
4. **Enriquecimento:** Aplicação automática das regras de negócio (`processor.py`) para categorização inicial.

## 5. Estrutura de Diretórios
```text
/
├── app.py              # Ponto de entrada (UI)
├── finance.db          # Base de dados (SQLite)
├── requirements.txt    # Dependências do projeto
├── src/                # Código fonte (lógica e backend)
│   ├── database.py     # Definição do Schema e Conexões
│   ├── utils.py        # ETL e Ingestão de CSVs
│   └── processor.py    # Algoritmo de Conciliação e Splits
└── docs/               # Documentação técnica
