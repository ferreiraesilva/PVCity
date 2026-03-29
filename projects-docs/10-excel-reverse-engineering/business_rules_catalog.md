# Catalogo inicial de regras de negocio

## Grafo funcional minimo
O nucleo real do workbook e formado por:
- Analise Proposta
- Permuta
- Fluxo
- PRC + COORD

## Regras-chave
### REG-A01. O workbook compara dois PVs para a mesma unidade e depende de contexto inicial obrigatorio
A planilha compara, para a mesma unidade imobiliaria:
- o PV padrao montado pela tabela base de venda
- o PV da proposta do cliente

Antes de qualquer simulacao, o usuario precisa:
- selecionar o empreendimento em `Analise Proposta!E5`
- selecionar a unidade desse empreendimento em `Analise Proposta!F8`
- informar a data base da analise em `Analise Proposta!E11`

A combinacao de `E5` com `F8` forma a chave derivada `E6`, aciona lookups em `Referencias` e `Tabela Venda - Parcela`, e preenche a base usada pelo calculo do PV padrao antes da edicao da proposta.

### REG-A02. A flag de permuta e estrutural
`Analise Proposta!N6` nao representa apenas um detalhe visual. Ela altera o trilho do calculo.
- Nao ativa o cenario normal
- Sim ativa o cenario com permuta

### REG-A03. O empreendimento define a estrutura do fluxo base; a unidade apenas troca a escala de valores
Na simulacao observada com `Garten|801`, `Garten|1001`, `Haut|801` e `Haut|1001`, a mudanca de unidade dentro do mesmo empreendimento nao alterou a arquitetura do fluxo.
- `Garten` preserva a mesma tabela-base: sinal, 3 entradas, mensais, semestrais, unica e financiamento bancario
- `Haut` preserva outra tabela-base: sinal, 3 entradas, sem mensais ativas, sem semestrais ativas, sem unica ativa e financiamento bancario

O que muda ao trocar a unidade e:
- preco total da unidade
- valor de cada parcela
- area privativa e demais dados da unidade

### REG-A04. A permuta reaproveita o fluxo da proposta e substitui a semestral por uma unica linha do tipo Permuta
Na leitura operacional adotada para o app:
- o fluxo com permuta nasce do mesmo cronograma da proposta normal
- a linha `Semestrais` e convertida em uma unica linha `Permuta`
- o valor da parcela de permuta e o mesmo valor unitario da parcela semestral
- o financiamento permanece ancorado no mesmo empreendimento/unidade

Esse comportamento foi observado como a principal variacao estrutural entre o trilho normal e o trilho com permuta nos cenarios comparados.

### REG-B01. A proposta e composta por linhas parametrizadas de parcela
Cada linha possui, no minimo:
- numero de parcelas
- periodicidade
- mes de inicio
- valor da parcela
- tipo/reajuste

### REG-C02. A ocorrencia de uma parcela e calculada por regra generica de cronograma
Para cada linha do cronograma mensal e para cada linha da proposta, o motor verifica:
- mes inicial
- quantidade de parcelas
- periodicidade
- distancia entre o mes da linha e o mes inicial

Se a ocorrencia for valida para aquele mes, o valor da parcela e lancado no bucket correspondente.

### REG-D02. Fixas Irreajustaveis mudam de bucket
Linhas marcadas como `Fixas Irreajustaveis` vao para o bucket irreajustavel. As demais seguem para o bucket reajustavel.

### REG-E01. Comissao direta e vinculada as linhas da proposta
A comissao direta do fluxo e montada por mes com base na coluna `Comissao + Premio (R$)` da grade da proposta.
- sem permuta usa Analise Proposta
- com permuta usa Permuta

### REG-E02. Comissao indireta e um evento financeiro proprio
A comissao indireta nao nasce diretamente da grade da proposta. Ela e lancada no fluxo em um mes especifico e depende da aba PRC + COORD.

### REG-E03. PRC + COORD redistribui a comissao total da proposta
A aba pega a comissao total e a distribui por papeis comerciais.

### REG-F03. O desconto nao e uniforme para todos os componentes
O motor distingue pelo menos:
- componente reajustavel
- componente irreajustavel
- comissao direta
- comissao indireta

### REG-G01. Permuta e segundo trilho do calculo
O workbook mantem:
- uma aba propria, Permuta
- uma tabela propria, Proposta8
- um bloco de fluxo proprio, tbFluxoPermuta
