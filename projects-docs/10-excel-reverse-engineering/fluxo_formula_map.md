# Mapeamento do Motor de Fluxo (Fórmulas e Comportamento)

## Objetivo
Documentar a interpretação rigorosa das fórmulas embutidas na tabela `tbFluxo` e `tbFluxoPermuta`, evidenciando a dependência posicional (linhas slotadas) avaliadas via funções `LET` e `SUMPRODUCT`. Não reinterpretar regras.

## 1. Fluxo Reajustável e Irreajustável (Colunas I e J)
O motor mensal do Excel não usa VBA, ele utiliza matrizes dinâmicas calculadas via cruzamento global entre o Mês vigente da iteração (linha atual do `tbFluxo`) e as matrizes completas da `Proposta` (ou `Proposta8`).

Para cada Mês (`tbFluxo[[#This Row],[Mês]]`), a planilha calcula um "Delta de Meses" ($d$) frente à Data de Início estipulada em cada slot da `Proposta`.
```excel
d = (AnoMes_Atual) - (AnoMes_Inicio + desloc_permuta)
```

O filtro temporal usa a matemática `MOD`:
- `MOD(d, passo) = 0`: Exige que o delta seja perfeitamente divisível pela frequência (1 p/ Mensal, 6 p/ Semestral, 12 p/ Anual).
- `d >= 0`: Garante que não compute parcelas no passado.
- `d / passo <= (n - 1)`: Garante que os lançamentos se encerrem após a quantidade `n` de parcelas estipulada.

O Valor Final no mês é o `SUMPRODUCT` desses booleanos multiplicados pelo Valor da Parcela.

### Trilho Normal X Trilho Permuta
- **Trilho Normal**: Lê o array derivado de `Analise Proposta!D38:N58`.
- **Trilho Permuta**: Lê o array derivado de `Permuta!D38:N58` (`Proposta8`). A lógica matricial temporal é idêntica (copiada/colada via `LET`), provando que a API precisa manter os payloads separados e injetar a lógica modular unificada.

## 2. Comissão Direta Mensal (Coluna K)
É computada somando a comissão devida *naquele mês*.
No Excel, isso é feito através de um `=SUMIFS('Analise Proposta'!$M:$M, ...)` onde a data de competência cai dentro do mês corrente do fluxo. Ou seja, ela é atrelada estritamente aos prazos de vencimento fixados na Tabela/Proposta. (Obs: No trilho Permuta, refere-se a `Permuta!$M:$M`).

## 3. Comissão Indireta Mensal (Coluna L)
Diferente da Comissão Direta (que flui no tempo), a Comissão Indireta é lançada como um evento financeiro de ocorrência **Singular** (Única) amarrada à Data de Entrega ou Marco Predefinido.
```excel
=IF( Mês_Atual == Mês_Target_Analise_Proposta, -'PRC + COORD'!$O$34*(1+$J$8), 0 )
```
O valor não advém da tabela da proposta. Ela herda da aba `PRC + COORD`, e é computada baseada num momento congelado, impactando consideravelmente a curva líquida no mês do seu disparo.

## Restrições Puxadas ao Código
- O código Python precisa simular o `SUMPRODUCT` (loop de matrizes) com a exata lógica matemática temporal. Abstrações de geração de parcelas iterativas com "For" são bem-vindas se, e somente se, o output final por mês colidir com o `SUMPRODUCT` no centavo.
