# Registro de Desenvolvimento - Gerenciador de Gastos

## [0.2.0] - 2026-06-24
### Adicionado
- **Suporte a OFX:** Implementada função de parser para arquivos OFX (padrão bancário internacional) via `ofxtools`.
- **Motor de Competência:** Nova lógica de fechamento dinâmico de fatura, permitindo o cálculo do período de competência baseado em dia de corte personalizado.
- **Auditoria de Fatura:** Nova métrica de consumo líquido (Gastos + Estornos) para validação cruzada com faturas oficiais.

### Alterado
- **Arquitetura de Ingestão:** Refatoração do módulo `utils.py` para normalizar dados provenientes de fontes heterogêneas (CSV/OFX).
- **Documentação:** Atualização técnica do `README.md` e `requisitos.md` para refletir as novas capacidades de integração.

## [0.1.0] - 2026-06-10
### Concluído
- Estrutura inicial do repositório.
- Camada de persistência (SQLite).
- Ingestão básica de CSV e interface (MVP).
- Motor de regras de classificação de transações.
