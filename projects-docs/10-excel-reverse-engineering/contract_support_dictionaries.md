# Dicionario minimo para sustentar contratos de API e catalogo de etapas

## Objetivo
Aprofundar somente os pontos da Template PV necessarios para:
- contratos de API
- step catalog operacional
- rastreabilidade de paridade

## Analise Proposta, campos essenciais

| Grupo logico | Campo logico | Origem Excel | Papel | Tipo | Valor observado | Impacto direto |
|---|---|---|---|---|---|---|
| Identificacao | empreendimento | `E5` | entrada | texto | `Garten` | chave principal para carregar unidade e tabela base |
| Identificacao | unidade | `F8` | entrada | texto | `601` | depende do empreendimento e compoe a chave `E6` |
| Identificacao | data base da analise | `E11` | entrada | data | `2026-03-10` | ancora o carregamento da tabela base e a simulacao dos cenarios de PV |
| Identificacao | chave produto-unidade | `E6` | derivado | texto | `Garten|601` | lookup em `Referencias` e `Tabela Venda - Parcela` |
| Identificacao | escaninho/garagem base | `H5` | derivado | texto | `E28` | informativo e documental |
| Identificacao | area privativa | `K5` | derivado | numero | `208.28` | base para decorado/facility |
| Identificacao | mes de entrega | `H11` | derivado | data | `2027-08-01` | ancora horizonte do fluxo e validacoes de financiamento |
| Flags | premio habilitado | `N4` | entrada | `Sim/Nao` | `Sim` | ativa `N9` e afeta comissao |
| Flags | toda faturada | `N5` | entrada | `Sim/Nao` | `Nao` | zera comissao total faturada em `R36` quando `Sim` |
| Flags | tem permuta | `N6` | entrada | `Sim/Nao` | `Nao` | altera total de comissao e ativa trilho `Permuta` |
| Comercial | gerente city | `K9` | entrada | texto | `Clara Soyer` | alimenta PRC + COORD |
| Comercial | imobiliaria | `K10` | entrada | texto | `Autonomo` | afeta desdobramento comercial |
| Comercial | corretor | `K11` | entrada | texto opcional | vazio | documentado, sem enum estavel nesta rodada |
| Comercial | gerente | `K12` | entrada | texto opcional | vazio | documentado, sem enum estavel nesta rodada |
| Comissao | rotulo principal | `M8` | entrada | texto | `Intermediada` | descritivo do bloco principal |
| Comissao | percentual principal | `N8` | derivado com override latente | numero | `0.05` | entra em `N12` |
| Comissao | premio rotulo | `M9` | derivado | texto | `Premio` | descritivo |
| Comissao | premio percentual | `N9` | derivado | numero | `0.005` | entra em `N12` |
| Comissao | slots secundarios | `M10:N11` | entrada opcional | texto + numero | vazio | entram em `N12` |
| Comissao | percentual total | `N12` | derivado | numero | `0.055` | resumo do percentual comercial |
| Modificacao | tipo de modificacao | `D20` | entrada | enum | `Nao` | altera `E8` e `J18` |
| Modificacao | decorado R$/m2 | `D21` | entrada | numero | `3300` | usado se `D20=Decorado (R$/m2)` |
| Modificacao | facility R$/m2 | `D22` | entrada | numero | `2700` | usado se `D20=Facility (R$/m2)` |
| Modificacao | area para modificacao | `D25` | entrada | numero | `208.28` | multiplicador de impacto no VGV |
| Proposal rows | linhas editaveis da proposta | `D38:N58` | entrada + derivado | grade slotada | varios | payload principal da API |
| Base rows | tabela base de venda | `F19:N27` | derivado | grade | varios | referencia de comparacao e defaults do PV padrao |
| Resultado | status PV | `H85` | derivado | texto | `PV Aprovado*` | criterio central do motor |
| Resultado | status comissao | `H86` | derivado | texto | `OK` | guard rail comercial |
| Resultado | status data financiamento | `H87` | derivado | texto | `OK` | valida coerencia entre tabela e proposta |
| Resultado | captacao total | `H88` | derivado | numero | `0.5` | insumo de risco |
| Resultado | risco | `H91` | derivado | texto | `Baixo` | resumo executivo |

## Analise Proposta, enumeracoes relevantes

| Campo | Origem | Valores observados ou validados |
|---|---|---|
| modificacao | validacao `D20` | `Nao`, `Decorado (R$/m2)`, `Facility (R$/m2)` |
| periodicidade | validacao `E39:E55` | `Sinal`, `Entrada`, `Mensais`, `Semestrais`, `Unica`, `Permuta`, `Anuais`, `Veiculo` |
| financiamento | validacao `E56:E58` | `Financ. Bancario`, `Financ. Direto` |
| booleanos | validacao `N4:N6` | `Sim`, `Nao` |

## Permuta, campos essenciais

| Grupo logico | Campo logico | Origem Excel | Papel | Tipo | Valor observado | Impacto direto |
|---|---|---|---|---|---|---|
| Reuso | empreendimento/unidade/contexto | `E5:K12` | derivado de `Analise Proposta` | misto | herdado | mantem coerencia entre trilhos |
| Permuta | variacao de VPL | `N6` | derivado | numero | `-0.7398747017` | resumo do ganho/perda do trilho |
| Permuta | diferenca de VGV | `N7` | derivado | numero | `1986431` | gap entre venda base e troca |
| Comissao | total permuta | `N14` | derivado | numero | `0.055` | resumo do trilho de permuta |
| Proposal rows | linhas da troca | `D38:N58` | entrada + derivado | grade slotada | varios | payload `exchange_flow_rows` |
| Resultado | status PV | `H90` | derivado | texto | `PV Reprovado` | resultado central da permuta |
| Resultado | status comissao | `H91` | derivado | texto | `OK` | guard rail comercial |
| Resultado | status data financiamento | `H92` | derivado | texto | `NAO OK` | coerencia do financiamento |
| Resultado | captacao total | `H93` | derivado | numero | `0.25` | insumo de risco |
| Resultado | risco | `H96` | derivado | texto | `Alto` | resumo executivo |

## Campos latentes ou com abertura necessaria

| Ponto | Origem | Situacao atual | Tratamento nesta rodada |
|---|---|---|---|
| override oculto de comissao | `Analise Proposta!U41:U42` | afeta `N8`, mas sem rotulo visivel nesta leitura | manter opcional em contrato, com warning |
| dropdown quebrado | `Analise Proposta!L12` | validacao aponta para `#REF!` | nao usar como enum estavel |
| flag de permuta sem rotulo claro | `Permuta!P95` | validacao `Sim/Nao`, sem dependencia observada | nao entrar como obrigatorio |
| formulas quebradas na metadata da tabela | tabela `Tabela` | XML contem `#REF!` em parte das formulas | usar celulas visiveis e comportamento efetivo |

## Decisao para a API
A API deve tratar `enterprise_name`, `unit_code` e `analysis_date` como o contexto minimo obrigatorio para abrir uma simulacao.

A API deve preservar dois arrays slotados:
1. `sale_flow_rows`, slots 39 a 58 da `Analise Proposta`
2. `exchange_flow_rows`, slots 39 a 58 da `Permuta`

Isso e mais aderente ao Excel do que abstrair uma lista livre de parcelas.
