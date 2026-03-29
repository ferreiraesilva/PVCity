# Lógica de Cálculo e Regras de Negócio

Este documento descreve as premissas financeiras e regras de validação utilizadas no motor de cálculo do PVCity.

## 1. Comparativo de Valor Presente (PV)

A eficiência de uma proposta não é medida pelo valor nominal bruto (VGV), mas sim pelo seu Valor Presente Líquido (VPL/PV).

### Fórmula de Variação de Eficiência
O sistema compara o PV da proposta do cliente contra o PV do fluxo padrão (tabela) da unidade selecionada.

$$Variação = \frac{PV_{Proposta}}{PV_{Padrão}} - 1$$

*   **PV Padrão**: Calculado a partir das parcelas originais cadastradas para a unidade no banco de dados, utilizando a taxa de desconto anual (VPL) definida para o produto.
*   **PV Proposta**: Calculado a partir das parcelas customizadas pelo vendedor.

> [!IMPORTANT]
> Esta abordagem garante uma comparação "maçãs com maçãs", pois ambos os fluxos são submetidos ao mesmo algoritmo de desconto financeiro.

## 2. Matriz de Nível de Risco

O nível de risco é uma combinação da saúde financeira (PV) e da exposição de caixa (Captura).

### Critérios de Risco
| Nível | PV Status | Captura Total |
| :--- | :--- | :--- |
| **Baixo** | Aprovado★ | $\ge$ Meta de Tabela |
| **Médio** | Aprovado | $\ge$ 50% da Meta de Tabela |
| **Alto** | Reprovado | < 50% da Meta de Tabela |

### Motivos de Risco (risk_reasons)
O sistema gera mensagens detalhadas para explicar o nível de risco:
*   **PV Financeiro Reprovado**: A variação de PV ficou abaixo do limite permitido para o empreendimento.
*   **PV Aprovado com ressalvas**: O PV exige alçada de gerente/diretor.
*   **Captura Crítica**: A entrada de caixa durante a obra está muito abaixo do esperado (Alto Risco).
*   **Captura Insuficiente**: A entrada de caixa está abaixo da meta, mas em um nível gerenciável (Médio Risco).

## 3. Captura Total

A métrica de captura indica o percentual do valor da unidade que entra no caixa da empresa antes do financiamento final.

$$Captura = 1 - \frac{\sum Parcelas_{Financiamento}}{VGV_{Total}}$$
