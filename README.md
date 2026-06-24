# Gerenciador de Gastos Inteligente

Uma solução avançada de controle financeiro voltada à conciliação bancária de alta precisão. Desenvolvida para superar as limitações de ferramentas convencionais, esta aplicação oferece uma camada de inteligência sobre extratos bancários, permitindo o tratamento de transações complexas, parcelamentos e a gestão de gastos em estabelecimentos híbridos.

## 🚀 O Diferencial Técnico

A maioria dos rastreadores de despesas baseia-se apenas na leitura passiva de dados. Este sistema implementa uma lógica de conciliação de competência, tratando o seu extrato não como uma simples lista, mas como um registro contábil de fatura.

* **Conciliação Multi-Fonte:** Suporte nativo para CSV e OFX (padrão bancário internacional), garantindo total integridade e rastreabilidade dos dados.
* **Fechamento Dinâmico:** Algoritmo proprietário que recalcula o período de competência baseado no dia de fechamento definido pelo usuário, permitindo bater a soma do sistema com o valor oficial do PDF da fatura.
* **Lógica de Resíduo (Smart Split):** Facilita a gestão de estabelecimentos híbridos, permitindo a segregação de gastos de forma inteligente.
* **Motor de Regras:** Classificação automática com reprocessamento em lote, permitindo que alterações nas regras de negócio atualizem instantaneamente todo o seu histórico financeiro.

## ⚙️ Funcionalidades

* **Ingestão Robusta (ETL):** Normalização de dados heterogêneos para um schema único no SQLite.
* **Dashboards Analíticos:** Visualização de gastos por categoria e período de competência.
* **Auditoria de Faturas:** Métricas em tempo real que permitem comparar o consumo líquido (gastos + estornos) com o valor final da fatura bancária.

## 🛠️ Stack Tecnológico

* **Linguagem:** Python 3.x
* **Interface:** Streamlit (UI reativa)
* **Engenharia de Dados:** Pandas (Manipulação de séries temporais)
* **Persistência:** SQLite (Banco relacional com integridade referencial)
* **Parsers Bancários:** `ofxtools` (Para processamento de arquivos OFX)

## 🏗️ Estrutura do Projeto

O sistema foi desenhado seguindo os princípios de baixo acoplamento e separação de responsabilidades:

1. **app.py**: Camada de apresentação e orquestração da UI.
2. **database.py**: Camada de persistência e gerenciamento do schema.
3. **processor.py**: Motor de regras de negócio e reclassificação.
4. **utils.py**: Módulos de ETL para normalização de CSV e OFX.

---
*Projeto desenvolvido como parte do curso de Engenharia de Computação.*
