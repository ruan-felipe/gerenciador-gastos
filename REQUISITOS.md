# Especificação de Requisitos: Gerenciador Financeiro

## 1. Visão Geral
Sistema avançado de controle financeiro e conciliação bancária de alta precisão. Projetado para gerenciar extratos bancários (Nubank) e lançamentos manuais, permitindo a gestão inteligente de estabelecimentos híbridos e o tratamento de transações complexas como parcelamentos.

## 2. Requisitos Funcionais (RF)
- **RF01:** Importação de extratos via CSV (padrão Nubank).
- **RF02:** Importação de extratos via OFX (padrão bancário internacional).
- **RF03:** Lançamento manual de despesas diárias para conciliação.
- **RF04:** Conciliação automática inteligente (Data e Valor).
- **RF05:** Split de gastos (divisão de valores em subcategorias).
- **RF06:** Cálculo automático de resíduo de transação.
- **RF07:** Fechamento dinâmico de fatura (cálculo baseado em dia de corte personalizado).
- **RF08:** Projeção e auditoria de valor final de fatura (consumo líquido).
- **RF09:** Reclassificação em lote baseada em motor de regras.

## 3. Regras de Negócio (RN)
- **RN01:** A soma dos "splits" não pode exceder o valor original da transação.
- **RN02:** Prioridade de classificação: Manual > Histórico > Regra Automática.
- **RN03:** O sistema deve sinalizar transações com "baixa confiança" de associação.
- **RN04:** O período de competência é determinado pelo dia de fechamento, recalculando automaticamente o mês de referência de cada transação.
- **RN05:** Estornos (valores negativos) devem ser processados como redutores do saldo líquido da fatura.

## 4. Estrutura do Banco
- **transactions:** Registro unificado de transações (Data, Título, Valor, Origem, Categoria).
- **rules:** Tabela de mapeamento de palavras-chave para classificação automática.
- **splits:** Registro de exceções para fatiamento de gastos.
- **establishment_profiles:** Definição de comportamento de locais (Híbridos/Simples).
- **categories:** Catálogo de classificação financeira.

## 5. Requisitos Não Funcionais (RNF)
- **RNF01:** Independência de fonte de dados (Normalização entre CSV/OFX).
- **RNF02:** Persistência de dados segura com SQLite e integridade referencial.
- **RNF03:** Modularidade do sistema (Camadas de ETL, Processamento e UI).
