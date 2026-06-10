# Especificação de Requisitos: Gerenciador Financeiro

## 1. Visão Geral
Sistema de conciliação financeira entre faturas bancárias (CSV) e lançamentos manuais diários, com foco em gestão de estabelecimentos híbridos.

## 2. Requisitos Funcionais
- **RF01:** Importação de CSV (Nubank).
- **RF02:** Lançamento manual de despesas diárias.
- **RF03:** Conciliação automática (Data ± 1 dia e Valor).
- **RF04:** Split de gastos (dividir valor total em sub-categorias).
- **RF05:** Cálculo de Resíduo automático.
- **RF06:** Projeção de gastos totais do mês.

## 3. Regras de Negócio
- **RN01:** A soma dos "splits" não pode exceder o valor original da transação.
- **RN02:** Prioridade de classificação: Manual > Histórico > Regra Automática.
- **RN03:** O sistema deve sinalizar transações com "baixa confiança" de associação.

## 4. Estrutura do Banco
- **transactions:** Registro bruto (CSV ou Manual).
- **categories:** Catálogo de categorias.
- **splits:** Tabela de exceções (fatias de gastos).
- **rules:** Mapeamento de palavras-chave.
- **establishment_profiles:** Definição de comportamento de locais (Híbridos/Simples).
