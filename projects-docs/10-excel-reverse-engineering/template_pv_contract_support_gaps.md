# Lacunas mínimas da planilha para sustentar contratos e step catalog

## Escopo desta abertura
Somente o que ainda precisa ser aberto para sustentar:
- `api_contracts_draft.md`
- `step_catalog.yaml`

## Lacunas mínimas

### 1. Override oculto da comissão principal
- Evidência: `Analise Proposta!N8` depende de `U41` e `U42`
- Problema: `U41:U42` não apareceu rotulado na leitura visível
- Impacto: existe um caminho alternativo para percentual da comissão principal
- Decisão desta rodada: manter como campo opcional `hidden_override` com warning de paridade

### 2. Validação quebrada em `L12`
- Evidência: a validação da célula aponta para `OFFSET(#REF!,MATCH(#REF!,#REF!,0)-1,0,COUNTIF(#REF!,#REF!),1)`
- Problema: não é fonte confiável para enumeração
- Impacto: não dá para congelar um contrato fechado para este campo com base só nesta evidência
- Decisão desta rodada: tratar como texto opcional até abrir a origem correta

### 3. Flag em `Permuta!P95`
- Evidência: existe validação `Sim/Não`
- Problema: nesta leitura não apareceu rótulo claro nem fórmula que consuma o campo
- Impacto: não deve entrar como obrigatório no contrato
- Decisão desta rodada: manter fora do payload obrigatório

### 4. Metadata da tabela `Tabela` com `#REF!`
- Evidência: o XML de `table5.xml` contém `#REF!` em colunas calculadas
- Problema: um agente pode tentar regenerar a regra pela metadata da tabela e divergir do comportamento visível da planilha
- Impacto: risco alto de implementação incorreta
- Decisão desta rodada: toda extração operacional deve confiar em células visíveis, fórmulas de worksheet e resultados observados, não na metadata da tabela

## O que não precisa ser aberto agora
- carta proposta
- layout de impressão
- integrações externas
- detalhes completos de PRC + COORD além do que já alimenta fluxo e resumo
