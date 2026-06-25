# Regras de Negócio e Lógica de Conciliação

## 1. Conceito Central: A Lógica de Resíduo
O sistema foi desenhado para resolver o problema de "estabelecimentos híbridos" (locais que vendem produtos de categorias distintas). Em vez de tentar categorizar o gasto total por uma única categoria genérica, o sistema prioriza o detalhamento manual.

**Fórmula de Cálculo:**
$$Resíduo = Valor\_Original\_Transação - \sum(Valores\_das\_Exceções)$$

*   **Valor_Original_Transação:** O valor capturado automaticamente do extrato bancário (CSV).
*   **Exceções (Splits):** Lançamentos manuais feitos pelo usuário para itens específicos dentro daquela mesma compra.
*   **Resíduo:** O valor remanescente que é automaticamente atribuído à "Categoria Padrão" do estabelecimento.

## 2. Lógica de Competência (Fatura)
O sistema não utiliza mais o mês civil padrão para agrupamento.
- **Regra de Corte:** Toda transação é vinculada a um "Período de Fatura" baseado no dia de fechamento configurado pelo usuário.
- **Recálculo Dinâmico:** Transações realizadas após o dia de corte são automaticamente atribuídas ao próximo período de competência.
- **Estornos:** Valores negativos são tratados como redutores do saldo líquido da fatura, garantindo a paridade com o extrato oficial do banco.

## 3. Fluxo de Integração (Multi-Fonte)
O sistema prioriza a integridade dos dados:
1. **Normalização:** Tanto arquivos CSV quanto OFX são convertidos para um *schema* unificado no banco de dados.
2. **Conciliação:** (Mantenha as seções anteriores de Matching e Perfis)
