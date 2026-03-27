# Catálogo inicial de regras de negócio

## Grafo funcional mínimo
O núcleo real do workbook é formado por:
- Analise Proposta
- Permuta
- Fluxo
- PRC + COORD

## Regras-chave
### REG-A02. A flag de permuta é estrutural
`Analise Proposta!N6` não representa apenas um detalhe visual. Ela altera o trilho do cálculo.
- Não ativa o cenário normal
- Sim ativa o cenário com permuta

### REG-B01. A proposta é composta por linhas parametrizadas de parcela
Cada linha possui, no mínimo:
- número de parcelas
- periodicidade
- mês de início
- valor da parcela
- tipo/reajuste

### REG-C02. A ocorrência de uma parcela é calculada por regra genérica de cronograma
Para cada linha do cronograma mensal e para cada linha da proposta, o motor verifica:
- mês inicial
- quantidade de parcelas
- periodicidade
- distância entre o mês da linha e o mês inicial
Se a ocorrência for válida para aquele mês, o valor da parcela é lançado no bucket correspondente.

### REG-D02. Fixas Irreajustaveis mudam de bucket
Linhas marcadas como `Fixas Irreajustaveis` vão para o bucket irreajustável. As demais seguem para o bucket reajustável.

### REG-E01. Comissão direta é vinculada às linhas da proposta
A comissão direta do fluxo é montada por mês com base na coluna `Comissão + Premio (R$)` da grade da proposta.
- sem permuta usa Analise Proposta
- com permuta usa Permuta

### REG-E02. Comissão indireta é um evento financeiro próprio
A comissão indireta não nasce diretamente da grade da proposta. Ela é lançada no fluxo em um mês específico e depende da aba PRC + COORD.

### REG-E03. PRC + COORD redistribui a comissão total da proposta
A aba pega a comissão total e a distribui por papéis comerciais.

### REG-F03. O desconto não é uniforme para todos os componentes
O motor distingue pelo menos:
- componente reajustável
- componente irreajustável
- comissão direta
- comissão indireta

### REG-G01. Permuta é segundo trilho do cálculo
O workbook mantém:
- uma aba própria, Permuta
- uma tabela própria, Proposta8
- um bloco de fluxo próprio, tbFluxoPermuta
