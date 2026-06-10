# Registro de Desenvolvimento - Gerenciador de Gastos

## [0.1.0] - 2026-06-10
### Concluído
- **Estrutura de Repositório:** Definição da hierarquia de pastas (src/, docs/).
- **Camada de Persistência:** Implementação de `database.py` (SQLite) com a estrutura correta para transações (`id`, `date`, `title`, `amount`, `category`, `source`).
- **Camada de Ingestão:** Implementação de `utils.py` com validação de formato de arquivo, tratamento de strings (limpeza de caracteres monetários) e conversão de tipos.
- **Interface (MVP):** `app.py` criado usando Streamlit, permitindo upload seguro de CSVs e integração com os módulos de processamento.
- **Validação de Segurança:** Tratamento de erros e limpeza de arquivos temporários implementados.

### Em Andamento / Próximo Passo
- **Motor de Processamento (`processor.py`):** Início da codificação da lógica de conciliação e cálculo de resíduo.
- **Visualização de Dados:** Integração do banco de dados com gráficos no dashboard.
