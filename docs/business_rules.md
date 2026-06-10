# Regras de Negócio e Lógica de Conciliação

## 1. Conceito Central: A Lógica de Resíduo
O sistema foi desenhado para resolver o problema de "estabelecimentos híbridos" (locais que vendem produtos de categorias distintas). Em vez de tentar categorizar o gasto total por uma única categoria genérica, o sistema prioriza o detalhamento manual.

**Fórmula de Cálculo:**
$$Resíduo = Valor\_Original\_Transação - \sum(Valores\_das\_Exceções)$$

*   **Valor_Original_Transação:** O valor capturado automaticamente do extrato bancário (CSV).
*   **Exceções (Splits):** Lançamentos manuais feitos pelo usuário para itens específicos dentro daquela mesma compra.
*   **Resíduo:** O valor remanescente que é automaticamente atribuído à "Categoria Padrão" do estabelecimento.

## 2. Fluxo de Conciliação (Matching)
O sistema opera em um fluxo de duas pontas que busca minimizar o erro humano:

### A. Registro (Input)
*   **Lançamentos Manuais:** Realizados via interface pelo usuário durante o mês.
*   **Ingestão CSV:** Processada mensalmente via extrato do Nubank.

### B. Matching Automático
O algoritmo de conciliação tenta associar registros manuais a registros do CSV utilizando os seguintes critérios:
1.  **Chave de Data:** O sistema busca registros manuais na mesma data (D) ou em um intervalo de tolerância (D +/- 1).
2.  **Chave de Valor:** Verifica se a soma das exceções manuais é menor que o valor total da transação do CSV.

### C. Níveis de Confiança
*   **Alta Confiança:** Registro manual encontrado para o mesmo dia e valor compatível. Conciliação realizada automaticamente.
*   **Baixa Confiança:** Divergências de data ou valor que excedem a margem de erro permitida. O sistema sinaliza o registro como "Pendente de Revisão" para o usuário.

## 3. Gestão de Perfis de Estabelecimento
Para automatizar o comportamento, o sistema utiliza perfis de locais:
*   **Perfil Simples:** Locais onde o gasto é recorrente e quase sempre na mesma categoria (ex: Assinatura de streaming).
*   **Perfil Complexo:** Locais onde a subdivisão de gastos é frequente (ex: Supermercados, Farmácias com conveniência, Postos de gasolina). Nesses locais, o sistema sempre solicita ou verifica a existência de *splits*.
