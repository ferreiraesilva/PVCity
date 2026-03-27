# Golden test cases iniciais de paridade

## Objetivo
Congelar os casos mínimos que o backend Python precisa reproduzir para provar equivalência funcional com a planilha `references/source-of-truth/Template PV - Março 26_v4.xlsx`.

## Regra de uso
1. Os valores esperados abaixo foram extraídos do workbook salvo, usando os valores persistidos na planilha.
2. O motor deve reproduzir esses resultados em `strict_excel_mode=true`.
3. Os casos abaixo são obrigatórios antes de avançar para implementação mais ampla.
4. Cada execução deve preservar `row_slot` de 39 a 58, sem reorder e sem compactação.

## Convenções desta suíte
- Datas em `YYYY-MM-DD`
- Percentuais em formato fracionário, por exemplo `0.055 = 5,5%`
- Valores monetários em BRL, comparados segundo `parity_rules.md`
- Campos textuais e status comparados de forma exata, após trim

## GT-001, cenário normal baseline do workbook

### Objetivo
Provar que o motor reproduz o trilho normal salvo hoje na Template PV.

### Fonte principal no Excel
- `Analise Proposta!E5:K12`
- `Analise Proposta!D20:D25`
- `Analise Proposta!D39:J58`
- `Analise Proposta!G83:H91`
- `Fluxo!G16:L98`

### Input lógico mínimo
```json
{
  "strict_excel_mode": true,
  "scenario_mode": "NORMAL",
  "product_context": {
    "enterprise_name": "Garten",
    "unit_code": "601",
    "product_unit_key": "Garten|601",
    "garage_code": "E28",
    "private_area_m2": 208.28,
    "analysis_date": "2026-03-26",
    "delivery_month": "2027-08-01",
    "modification_kind": "Não",
    "decorated_value_per_m2": 3300.0,
    "facility_value_per_m2": 2700.0,
    "area_for_modification_m2": 208.28,
    "prize_enabled": true,
    "fully_invoiced": false,
    "has_permuta": false
  },
  "commercial_context": {
    "city_sales_manager_name": "Clara Soyer",
    "real_estate_name": "Autônomo",
    "broker_name": null,
    "manager_name": null
  },
  "commission_context": {
    "primary_commission_label": "Intermediada",
    "primary_commission_percent": 0.05,
    "prize_commission_label": "Prêmio",
    "prize_commission_percent": 0.005,
    "secondary_commission_slots": [
      {"slot": 1, "label": null, "percent": null},
      {"slot": 2, "label": null, "percent": null}
    ],
    "hidden_override": {
      "enabled": null,
      "override_percent": null
    }
  }
}
```

### Sale flow rows obrigatórias
Comparar no mínimo estes slots:

| row_slot | installment_count | periodicity | start_month | installment_value | percent | total_vgv | adjustment_type |
|---|---:|---|---|---:|---:|---:|---|
| 39 | 1 | Sinal | 2026-03-10 | 108673.84 | 0.04 | 108673.84 | Fixas Irreajustaveis |
| 40 | 1 | Entrada | 2026-04-10 | 81505.38 | 0.03 | 81505.38 | Fixas Irreajustaveis |
| 41 | 1 | Entrada | 2026-05-10 | 81505.38 | 0.03 | 81505.38 | Fixas Irreajustaveis |
| 42 | 1 | Entrada | 2026-06-10 | 81505.38 | 0.03 | 81505.38 | Fixas Irreajustaveis |
| 43 | 14 | Mensais | 2026-07-10 | 38812.085714285706 | 0.014285714285714282 | 543369.1999999998 | INCC |
| 44 | 2 | Semestrais | 2026-09-10 | 135842.30000000002 | 0.05 | 271684.60000000003 | INCC |
| 45 | 1 | Única | 2027-03-10 | 190179.22000000003 | 0.07 | 190179.22000000003 | INCC |
| 56 | 1 | Financ. Bancário | 2027-11-10 | 1358423.0 | 0.5 | 1358423.0 | IGPM + 12% a.a |

### Saída esperada crítica
#### Resumo
| Campo lógico | Origem Excel | Esperado |
|---|---|---|
| pv_status | `Analise Proposta!H85` | `PV Aprovado*` |
| commission_status | `Analise Proposta!H86` | `OK` |
| financing_date_status | `Analise Proposta!H87` | `OK` |
| capture_total | `Analise Proposta!H88` | `0.5` |
| risk_status | `Analise Proposta!H91` | `Baixo` |

#### Comissão
| Campo lógico | Origem Excel | Esperado |
|---|---|---:|
| total_commission_percent | `Analise Proposta!R36` | 0.055 |
| total_commission_value | `Analise Proposta!R35` | 149426.53 |

#### Fluxo mensal normal, pontos de conferência
| Mês | Origem Excel | Fluxo reajustável | Fluxo irreajustável | Comissão direta | Comissão indireta |
|---|---|---:|---:|---:|---:|
| Total | `Fluxo!I17:L17` | 2363656.02 | 353189.98 | 0 | -104544.23407999998 |
| 2026-03-01 | `Fluxo!I18:L18` | 0 | 108673.84 | 0 | -104544.23407999998 |
| 2026-09-01 | `Fluxo!I24:L24` | 174654.38571428572 | 0 | 0 | 0 |
| 2027-03-01 | `Fluxo!I30:L30` | 364833.60571428575 | 0 | 0 | 0 |
| 2027-11-01 | `Fluxo!I38:L38` | 0 | 0 | 0 | 0 |

### Critério de aprovação do caso
O caso passa quando:
- o resumo crítico casa com o Excel
- os slots acima casam com o Excel
- os totais do fluxo mensal casam com o Excel
- o motor devolve `warnings=[]` ou apenas warnings informativos não impeditivos
- `parity_trace` aponta explicitamente para as células de origem comparadas

## GT-002, cenário com permuta baseline do workbook

### Objetivo
Provar que o motor reproduz o trilho de permuta salvo hoje na Template PV.

### Fonte principal no Excel
- `Permuta!N6:N14`
- `Permuta!D39:J58`
- `Permuta!G88:H96`
- `Fluxo!G105:L187`

### Input lógico mínimo
Igual ao caso GT-001, com estas diferenças obrigatórias:
```json
{
  "scenario_mode": "PERMUTA",
  "product_context": {
    "has_permuta": true
  }
}
```

### Exchange flow rows obrigatórias
| row_slot | installment_count | periodicity | start_month | installment_value | percent | total_vgv | adjustment_type |
|---|---:|---|---|---:|---:|---:|---|
| 39 | 1 | Sinal | 2026-03-10 | 51129.05 | 0.07 | 51129.05 | Fixas Irreajustaveis |
| 40 | 1 | Entrada | 2026-04-10 | 43824.9 | 0.06 | 43824.9 | Fixas Irreajustaveis |
| 41 | 1 | Entrada | 2026-05-10 | 43824.9 | 0.06 | 43824.9 | Fixas Irreajustaveis |
| 42 | 1 | Entrada | 2026-06-10 | 43824.9 | 0.06 | 43824.9 | Fixas Irreajustaveis |
| 43 | 0 | Mensais | 2026-03-10 | 0 | 0 | 0 | INCC |
| 44 | 0 | Semestrais | 2026-09-10 | 0 | 0 | 0 | INCC |
| 45 | 0 | Única | 2026-06-10 | 0 | 0 | 0 | INCC |
| 56 | 1 | Financ. Bancário | 2026-07-10 | 547811.25 | 0.75 | 547811.25 | IGPM + 12% a.a |

### Saída esperada crítica
#### Resumo permuta
| Campo lógico | Origem Excel | Esperado |
|---|---|---|
| pv_status | `Permuta!H90` | `PV Reprovado` |
| commission_status | `Permuta!H91` | `OK` |
| financing_date_status | `Permuta!H92` | `NÃO OK` |
| capture_total | `Permuta!H93` | `0.25` |
| risk_status | `Permuta!H96` | `Alto` |

#### Indicadores de permuta
| Campo lógico | Origem Excel | Esperado |
|---|---|---:|
| vpl_variation | `Permuta!N6` | -0.7398747017153582 |
| vgv_difference | `Permuta!N7` | 1986431 |
| total_commission_percent | `Permuta!N14` | 0.055 |
| exchange_total_vgv | `Permuta!I59` | 730415 |

#### Fluxo mensal permuta, pontos de conferência
| Mês | Origem Excel | Fluxo reajustável | Fluxo irreajustável | Comissão direta | Comissão indireta |
|---|---|---:|---:|---:|---:|
| Total | `Fluxo!I106:L106` | 547811.25 | 182603.75 | 0 | -104544.23407999998 |
| 2026-03-01 | `Fluxo!I107:L107` | 0 | 51129.05 | 0 | -104544.23407999998 |
| 2026-07-01 | `Fluxo!I111:L111` | 547811.25 | 0 | 0 | 0 |
| 2026-09-01 | `Fluxo!I113:L113` | 0 | 0 | 0 | 0 |

### Critério de aprovação do caso
O caso passa quando:
- o resumo de permuta casa com o Excel
- os slots acima casam com o Excel
- os totais do fluxo mensal de permuta casam com o Excel
- o motor devolve `warnings` somente para campos latentes não usados ou não evidenciados
- `parity_trace` aponta explicitamente para as células de origem comparadas

## Casos candidatos, não bloqueantes nesta rodada
Estes casos devem entrar depois, mas não impedem o início do backend:
1. comissão principal com override oculto habilitado em `Analise Proposta!U41:U42`
2. `fully_invoiced=true` zerando `% de comissão` em `Analise Proposta!R36`
3. alteração de `modification_kind` para `Decorado (R$/m²)` e `Facility (R$/m²)`
4. cenário com financiamento direto nas linhas 56 a 58
5. cenário em que `P95` da aba `Permuta` se prove relevante
