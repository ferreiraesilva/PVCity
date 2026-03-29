# Regras de paridade para o motor Python

## Objetivo
Definir como o motor do MVP deve comparar sua saída com a planilha `Template PV - Março 26_v4.xlsx` sem inventar regra nem aceitar divergência escondida.

## Regra de ouro
A paridade é medida contra o comportamento efetivo do workbook, não contra abstrações desejadas no código.

## Escopo desta versão
Estas regras cobrem:
- comparação do resumo normal e do resumo com permuta
- comparação de linhas slotadas da proposta
- comparação do fluxo mensal
- tolerâncias numéricas
- tratamento de vazios, warnings e campos latentes

## Ordem de precedência
1. valor efetivo salvo no workbook
2. fórmula visível de worksheet que explica esse valor
3. artefatos documentais do projeto
4. interpretação de implementação

Se houver conflito entre 3 e 1, vence 1.

## Unidades de comparação

### 1. Campos textuais e status
Comparação exata após:
- trim
- normalização de quebra de linha para espaço simples

Não normalizar acentuação.  
`NÃO OK` e `NAO OK` são diferentes.

### 2. Datas
Comparar por data calendário em `YYYY-MM-DD`.  
Ignorar horário quando o workbook trouxer `00:00:00`.

### 3. Valores monetários
Usar tolerância absoluta de `0.01`.

Exemplos:
- `149426.53` e `149426.5300001` passam
- `149426.53` e `149426.55` falham

### 4. Percentuais e razões
Usar tolerância absoluta de `0.00000001`.

Exemplos:
- `0.03` e `0.0299999999` passam
- `0.5` e `0.5001` falham

### 5. Campos nulos, vazios e zero
Não tratar tudo como equivalente.

#### Podem ser normalizados para `null`
- `installment_count`
- `periodicity`
- `start_month`
- `installment_value`
- `notes`

#### Devem permanecer `0` quando computados
- `percent`
- `total_vgv`
- buckets mensais de fluxo
- comissão direta mensal
- comissão indireta mensal

## Regra estrutural obrigatória, row slots

### Slots do trilho normal
O motor deve preservar `sale_flow_rows` de `39` a `58`.

### Slots do trilho de permuta
O motor deve preservar `exchange_flow_rows` de `39` a `58`.

### O que é proibido
- reordenar parcelas
- remover linhas vazias
- compactar linhas não usadas
- reconstruir o cronograma ignorando o slot original

## Campos críticos obrigatórios por suíte

### Resumo normal
Comparar obrigatoriamente:
- `pv_status`
- `commission_status`
- `financing_date_status`
- `capture_total`
- `risk_status`

### Resumo permuta
Comparar obrigatoriamente:
- `pv_status`
- `commission_status`
- `financing_date_status`
- `capture_total`
- `risk_status`
- `vpl_variation`
- `vgv_difference`

### Comissão
Comparar obrigatoriamente:
- percentual total da comissão
- valor total da comissão
- comissão indireta do primeiro mês impactado

### Fluxo mensal
Comparar obrigatoriamente:
- total do fluxo reajustável
- total do fluxo irreajustável
- total da comissão direta
- total da comissão indireta
- meses explicitamente marcados nos golden cases

## Regras sensíveis que exigem `parity_trace`

### 1. Comissão total
O motor deve provar o caminho de:
- `N8:N12`
- `R36`
- `R35`

No caso normal baseline, o percentual total esperado é `0.055` e o valor total é `149426.53`.

### 2. Cap sequencial da comissão por ordem de linha
As linhas `Q39:Q48` e `R39:R48` mostram que a comissão é travada por ordem de linha e por limite acumulado.  
Isto impede uma implementação que distribua comissão por algoritmo genérico sem respeitar a sequência do Excel.

### 3. Toda faturada
`Analise Proposta!R36` depende de `N5`.  
Se `N5="Sim"`, a comissão percentual total vai para zero.

### 4. Prêmio
`Analise Proposta!N9` depende de `N4`.  
Se `N4="Sim"`, entra `0.5%`.  
Se `N4="Não"`, entra `0`.

### 5. Permuta influencia comissão total
`Analise Proposta!N12` tem ramo explícito para `N6="Sim"`.  
Não tratar a comissão da permuta como cálculo isolado sem reflexo no contrato principal.

### 6. Tipo de reajuste em financiamento
Nas linhas `56:58`, o `adjustment_type` muda conforme `periodicity/financing_kind`.
O motor deve devolver o tipo observado pelo Excel, não um enum inferido por regra externa.

### 7. Risco
O risco não deve ser recalculado por heurística separada.
Ele precisa seguir a lógica efetiva do workbook a partir do resultado de PV e de captação.

## Warnings obrigatórios

### Quando emitir warning
Emitir warning, sem bloquear cálculo, quando houver:
- uso potencial de campo latente sem rótulo claro
- dropdown quebrado ou não confiável
- diferença entre metadata de tabela e fórmula visível da worksheet
- payload incompleto que o motor conseguiu completar por default conhecido

### Warnings já conhecidos nesta rodada
1. `hidden_override_commission_rule_unverified`
   - relacionado a `Analise Proposta!U41:U42`

2. `broken_validation_source_l12`
   - relacionado a `Analise Proposta!L12`

3. `permuta_flag_p95_unverified`
   - relacionado a `Permuta!P95`

4. `table_metadata_ref_not_trusted`
   - relacionado a `table5.xml` com `#REF!`

## Regras para leitura do source of truth
- confiar em células visíveis, fórmulas de worksheet e valores efetivos salvos
- não confiar na metadata quebrada de tabela para regenerar regra
- não substituir o workbook original por uma versão recalculada
- quando precisar de recálculo real, gerar uma cópia recalculada e distingui-la explicitamente da inspeção estrutural do arquivo original
- não arredondar cedo demais durante o cálculo
- não trocar decimal fracionário por percentual textual durante a comparação

## Contrato mínimo de `parity_trace`
Cada resposta de cálculo sensível deve permitir rastrear:
- `field`
- `actual_value`
- `expected_value` quando houver contexto de teste
- `excel_sheet`
- `excel_cell_or_range`
- `rule_note`

### Exemplo mínimo
```json
[
  {
    "field": "summary.normal.pv_status",
    "actual_value": "PV Aprovado*",
    "excel_sheet": "Analise Proposta",
    "excel_cell_or_range": "H85",
    "rule_note": "Resultado de PV do cenário normal"
  },
  {
    "field": "summary.permuta.vpl_variation",
    "actual_value": -0.7398747017153582,
    "excel_sheet": "Permuta",
    "excel_cell_or_range": "N6",
    "rule_note": "Variação de VPL do cenário de permuta"
  }
]
```

## Falhas que devem reprovar o teste imediatamente
Reprovar sem relativização quando houver:
- mudança de status de PV, comissão, financiamento ou risco
- divergência de slot
- divergência de mês no fluxo
- divergência acima da tolerância em totais
- ausência de campo crítico esperado
- uso de regra inventada não respaldada pelo workbook

## O que ainda pode ficar fora desta rodada
- carta proposta
- layout de impressão
- integrações externas
- trilhas além do baseline salvo hoje
