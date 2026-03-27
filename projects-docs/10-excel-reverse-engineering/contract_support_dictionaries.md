# Dicionário mínimo para sustentar contratos de API e catálogo de etapas

## Objetivo
Aprofundar somente os pontos da Template PV necessários para:
- contratos de API
- step catalog operacional
- rastreabilidade de paridade

## Analise Proposta, campos essenciais

| Grupo lógico | Campo lógico | Origem Excel | Papel | Tipo | Valor observado | Impacto direto |
|---|---|---|---|---|---|---|
| Identificação | empreendimento | `E5` | entrada | texto | `Garten` | chaves de lookup em referências e tabela de venda |
| Identificação | unidade | `F8` | entrada | texto | `601` | compõe chave `E6` |
| Identificação | chave produto-unidade | `E6` | derivado | texto | `Garten|601` | lookup em `Referencias` e `Tabela Venda - Parcela` |
| Identificação | escaninho/garagem base | `H5` | derivado | texto | `E28` | informativo e documental |
| Identificação | área privativa | `K5` | derivado | número | `208.28` | base para decorado/facility |
| Flags | prêmio habilitado | `N4` | entrada | `Sim/Não` | `Sim` | ativa `N9` e afeta comissão |
| Flags | toda faturada | `N5` | entrada | `Sim/Não` | `Não` | zera comissão total faturada em `R36` quando `Sim` |
| Flags | tem permuta | `N6` | entrada | `Sim/Não` | `Não` | altera total de comissão e ativa trilho `Permuta` |
| Comercial | gerente city | `K9` | entrada | texto | `Clara Soyer` | alimenta PRC + COORD |
| Comercial | imobiliária | `K10` | entrada | texto | `Autônomo` | afeta desdobramento comercial |
| Comercial | corretor | `K11` | entrada | texto opcional | vazio | documentado, sem enum estável nesta rodada |
| Comercial | gerente | `K12` | entrada | texto opcional | vazio | documentado, sem enum estável nesta rodada |
| Comissão | rótulo principal | `M8` | entrada | texto | `Intermediada` | descritivo do bloco principal |
| Comissão | percentual principal | `N8` | derivado com override latente | número | `0.05` | entra em `N12` |
| Comissão | prêmio rótulo | `M9` | derivado | texto | `Prêmio` | descritivo |
| Comissão | prêmio percentual | `N9` | derivado | número | `0.005` | entra em `N12` |
| Comissão | slots secundários | `M10:N11` | entrada opcional | texto + número | vazio | entram em `N12` |
| Comissão | percentual total | `N12` | derivado | número | `0.055` | resumo do percentual comercial |
| Modificação | tipo de modificação | `D20` | entrada | enum | `Não` | altera `E8` e `J18` |
| Modificação | decorado R$/m² | `D21` | entrada | número | `3300` | usado se `D20=Decorado (R$/m²)` |
| Modificação | facility R$/m² | `D22` | entrada | número | `2700` | usado se `D20=Facility (R$/m²)` |
| Modificação | área para modificação | `D25` | entrada | número | `208.28` | multiplicador de impacto no VGV |
| Proposal rows | linhas editáveis da proposta | `D38:N58` | entrada + derivado | grade slotada | vários | payload principal da API |
| Base rows | tabela base de venda | `F19:N27` | derivado | grade | vários | referência de comparação e defaults |
| Resultado | status PV | `H85` | derivado | texto | `PV Aprovado*` | critério central do motor |
| Resultado | status comissão | `H86` | derivado | texto | `OK` | guard rail comercial |
| Resultado | status data financiamento | `H87` | derivado | texto | `OK` | valida coerência entre tabela e proposta |
| Resultado | captação total | `H88` | derivado | número | `0.5` | insumo de risco |
| Resultado | risco | `H91` | derivado | texto | `Baixo` | resumo executivo |

## Analise Proposta, enumerações relevantes

| Campo | Origem | Valores observados ou validados |
|---|---|---|
| modificação | validação `D20` | `Não`, `Decorado (R$/m²)`, `Facility (R$/m²)` |
| periodicidade | validação `E39:E55` | `Sinal`, `Entrada`, `Mensais`, `Semestrais`, `Única`, `Permuta`, `Anuais`, `Veículo` |
| financiamento | validação `E56:E58` | `Financ. Bancário`, `Financ. Direto` |
| booleanos | validação `N4:N6` | `Sim`, `Não` |

## Permuta, campos essenciais

| Grupo lógico | Campo lógico | Origem Excel | Papel | Tipo | Valor observado | Impacto direto |
|---|---|---|---|---|---|---|
| Reuso | empreendimento/unidade/contexto | `E5:K12` | derivado de `Analise Proposta` | misto | herdado | mantém coerência entre trilhos |
| Permuta | variação de VPL | `N6` | derivado | número | `-0.7398747017` | resumo do ganho/perda do trilho |
| Permuta | diferença de VGV | `N7` | derivado | número | `1986431` | gap entre venda base e troca |
| Comissão | total permuta | `N14` | derivado | número | `0.055` | resumo do trilho de permuta |
| Proposal rows | linhas da troca | `D38:N58` | entrada + derivado | grade slotada | vários | payload `exchange_flow_rows` |
| Resultado | status PV | `H90` | derivado | texto | `PV Reprovado` | resultado central da permuta |
| Resultado | status comissão | `H91` | derivado | texto | `OK` | guard rail comercial |
| Resultado | status data financiamento | `H92` | derivado | texto | `NÃO OK` | coerência do financiamento |
| Resultado | captação total | `H93` | derivado | número | `0.25` | insumo de risco |
| Resultado | risco | `H96` | derivado | texto | `Alto` | resumo executivo |

## Campos latentes ou com abertura necessária

| Ponto | Origem | Situação atual | Tratamento nesta rodada |
|---|---|---|---|
| override oculto de comissão | `Analise Proposta!U41:U42` | afeta `N8`, mas sem rótulo visível nesta leitura | manter opcional em contrato, com warning |
| dropdown quebrado | `Analise Proposta!L12` | validação aponta para `#REF!` | não usar como enum estável |
| flag de permuta sem rótulo claro | `Permuta!P95` | validação `Sim/Não`, sem dependência observada | não entrar como obrigatório |
| fórmulas quebradas na metadata da tabela | tabela `Tabela` | XML contém `#REF!` em parte das fórmulas | usar células visíveis e comportamento efetivo |

## Decisão para a API
A API deve preservar dois arrays slotados:
1. `sale_flow_rows`, slots 39 a 58 da `Analise Proposta`
2. `exchange_flow_rows`, slots 39 a 58 da `Permuta`

Isso é mais aderente ao Excel do que abstrair uma lista livre de parcelas.
