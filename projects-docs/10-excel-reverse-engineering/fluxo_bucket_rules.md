# Regras de Bucket Financeiro do Mês

## Objetivo
Consolidar e separar logicamente os Buckets baseando-se no que a fonte de verdade (`tbFluxo`) alocou internamente por regra estrita de tipo.

## Classificação de Reajustável e Irreajustável
Conforme evidenciado no Output do Motor (`EXCEL-04`), o campo string de "Tipo/Reajuste" da linha da proposta é o pivot (Chave de Separação) da distribuição.

### Regra Matricial
* `_xlpm.fixa_irreaj` captura um booleano quando `tipo = "fixas irreajustaveis"`.
* O cálculo *Reajustável* (Coluna I) varre todas as linhas multiplicando pela diretiva `(1 - fixa_irreaj)` e avaliando se a string não está vazia.
* O cálculo *Irreajustável* (Coluna J) captura apenas onde `_xlpm.fixas = (tipo="Fixas Irreajustaveis")*(inicio<>"")`.

**Atenção aos Buckets**: O valor NUNCA é segmentado (uma parte reajusta, uma parte fixa na mesma linha de payload da proposta). A linha slotada INTEIRA vai para um Bucket, ou vai para o outro (Binário puro).

## Buckets e suas Taxas de Desconto
O fluxo não se resume a apenas transpor os valores em colunas. As taxas de desconto ao Valor Presente (PV) interagem de formas autônomas em cima dos buckets:
1. **Fluxo Irreajustável (O e T):** Seu PV desconta usando fórmulas agregadoras envolvendo as taxas compostas vigentes ($J$6 e $J$7) mescladas via uma mecânica `((1+(((1+$J$6)^(1/12))*((1+$J$7)^(1/12))-1))^Mês)`.
2. **Fluxo Reajustável (N e S):** Usa rotas de desconto mais secas `I18/((1+$J$7)^(1/12))^F18`.

## Tratamento da Comissão (Dedução Seca)
A Comissão Direta não reajusta dentro dos cálculos, operando sua dedução estaticamente na agregação das colunas M ou Q. O mesmo ocorre para a Comissão Indireta. Ambas são redutoras do Valor da Parcela Paga.

## Diferença de Buckets em Paridade Permuta
O fluxo de permuta (`tbFluxoPermuta`) retém o exato maquinário comportamental. A única exceção de alocação temporal e "deslocador" do Motor de Bucket é a rotina `_xlpm.desloc_permuta, IF(_xlpm.freq="permuta",12,0)`. Se a periodicidade lida for explícita para "permuta", ele retrocede/avança os deltas, impondo uma regra que os programadores não podem deixar de incluir no Python sob o risco do VPL (Valor Presente Líquido) deslocar erroneamente por 1 ano.
