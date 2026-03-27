# Contratos de API, rascunho operacional aderente à Template PV

## Objetivo deste artefato
Detalhar contratos de API suficientes para iniciar implementação guiada por agentes, preservando paridade com a planilha `Template PV - Março 26_v4.xlsx`.

## Guard rails obrigatórios
1. A planilha continua sendo a única fonte de verdade da regra.
2. O backend não pode reinterpretar a regra com abstrações livres antes de preservar a semântica do Excel.
3. O contrato principal deve preservar ordem e slot das linhas editáveis da planilha.
4. Permuta entra no contrato principal, não como extensão futura.
5. O modo padrão é `strict_excel_mode=true`.
6. Sempre que um campo depender de célula oculta, vazia ou sem rótulo claro, isso deve sair em `warnings` e em `parity_trace`.

## Recorte coberto nesta rodada
Este rascunho cobre:
- bootstrap mínimo para tela e motor
- cálculo principal normal e com permuta
- persistência mínima do cenário
- retorno de rastreabilidade para paridade

Não cobre ainda:
- geração de carta proposta em PDF/DOC
- workflow comercial completo
- integrações externas
- autenticação e autorização

## Princípio estrutural do payload
O payload principal usa duas ideias para aderir ao Excel:
1. **contexto do produto e da venda**, mapeado para células de topo
2. **linhas slotadas**, preservando a lógica das linhas 39 a 58 da tabela `Proposta` e da tabela `Proposta8`

Isso evita que o agente trate a proposta como um array livre e quebre dependências por posição, especialmente nas fórmulas de comissão e no fluxo mensal.

## Mapeamento de blocos do contrato para o Excel

| Bloco do contrato | Origem principal no Excel | Observação |
|---|---|---|
| `product_context` | `Analise Proposta!E5:F8`, `H5`, `K5`, `E11`, `H11`, `D20:D25`, `N4:N6` | Contexto inicial da análise |
| `commercial_context` | `Analise Proposta!K9:K12` | Estrutura comercial exibida no topo |
| `commission_context` | `Analise Proposta!M8:N12`, `Q54:X54`, auxiliares `U41:U42` | Há parte explícita e parte latente |
| `base_sale_table_rows` | tabela `Tabela` em `Analise Proposta!F19:N27` | Base vinda da tabela de vendas |
| `sale_flow_rows` | tabela `Proposta` em `Analise Proposta!D38:N58` | Trilho normal |
| `exchange_flow_rows` | tabela `Proposta8` em `Permuta!D38:N58` | Trilho de permuta |
| `sale_monthly_flow` | `Fluxo!G16:L98` via tabela `tbFluxo` | Fluxo mensal normal |
| `exchange_monthly_flow` | `Fluxo!G105:L187` via tabela `tbFluxoPermuta` | Fluxo mensal de permuta |
| `summary.normal` | `Analise Proposta!G83:H91` | Resultado da proposta normal |
| `summary.permuta` | `Permuta!G88:H96` | Resultado do cenário com permuta |
| `indirect_commission` | `PRC + COORD!O34` e derivadas em `Fluxo` | Comissão indireta do mês da entrega |

## Enumerações já observadas na planilha

### Booleanos
- `Sim`
- `Não`

### Modificação
Origem observada: validação de `Analise Proposta!D20`
- `Não`
- `Decorado (R$/m²)`
- `Facility (R$/m²)`

### Periodicidade
Origem observada: validação de `Analise Proposta!E39:E55` e `Permuta!E39:E55`
- `Sinal`
- `Entrada`
- `Mensais`
- `Semestrais`
- `Única`
- `Permuta`
- `Anuais`
- `Veículo`

### Tipo de financiamento
Origem observada: validação de `E56:E58`
- `Financ. Bancário`
- `Financ. Direto`

### Tipo/Reajuste observado
- `Fixas Irreajustaveis`
- `INCC`
- `IGPM + 12% a.a`
- `IPCA + 0,99% a.m`
- `IPCA + 13,65% a.a`

## Endpoint 1, bootstrap mínimo de referência

### `GET /api/v1/bootstrap/reference-data`
Objetivo: entregar os dados mínimos para montar a tela inicial e popular seletores.

### Response
```json
{
  "products": [
    {
      "enterprise_name": "Garten",
      "work_code": "6101I",
      "spe_name": "SPE RESIDENCIAL CITY 17 EMPREENDIMENTOS LTDA",
      "default_discount_percent": 0.08,
      "default_vpl_rate_annual": 0.10,
      "delivery_month": "2027-08-01",
      "launch_date": "2023-09-24",
      "stage": "Remanescente",
      "personalization_status": "Finalizada",
      "personalization_deadline": null
    }
  ],
  "unit_lookup_keys": [
    {
      "product_unit_key": "Garten|601",
      "enterprise_name": "Garten",
      "unit_code": "601",
      "unit_type": "Padrão",
      "suites": 3,
      "private_area_m2": 208.28,
      "garage_spots": "41/41A/45",
      "base_price": 2716846.0,
      "status": "Disponível"
    }
  ],
  "real_estate_agencies": [
    {
      "name": "Autônomo",
      "manager_cv_name": null
    }
  ],
  "enums": {
    "boolean_ptbr": ["Sim", "Não"],
    "modification_kind": ["Não", "Decorado (R$/m²)", "Facility (R$/m²)"],
    "periodicity": ["Sinal", "Entrada", "Mensais", "Semestrais", "Única", "Permuta", "Anuais", "Veículo"],
    "financing_kind": ["Financ. Bancário", "Financ. Direto"]
  }
}
```

### Fonte de cada parte
- `products`: aba `tbCadastroProduto`
- `unit_lookup_keys`: aba `Referencias`
- `real_estate_agencies`: aba `Imobs`
- `enums`: validações observadas nas abas `Analise Proposta` e `Permuta`

## Endpoint 2, carregar defaults da unidade

### `GET /api/v1/products/{enterprise_name}/units/{unit_code}/defaults`
Objetivo: devolver o estado inicial da análise antes de edição humana.

### Response contract
```json
{
  "product_context": {
    "enterprise_name": "Garten",
    "unit_code": "601",
    "product_unit_key": "Garten|601",
    "garage_code": "E28",
    "private_area_m2": 208.28,
    "delivery_month": "2027-08-01",
    "default_analysis_date_kind": "server_today",
    "default_modification_kind": "Não",
    "default_decorated_value_per_m2": 3300.0,
    "default_facility_value_per_m2": 2700.0,
    "default_area_for_modification_m2": 208.28,
    "default_prize_enabled": true,
    "default_fully_invoiced": false,
    "default_has_permuta": false
  },
  "base_sale_table_rows": [
    {
      "row_slot": 20,
      "installment_count": 1,
      "periodicity": "Sinal",
      "start_month": "2026-03-10",
      "installment_value": 108673.84,
      "percent": 0.04,
      "total_vgv": 108673.84,
      "commission_target_value": 104598.571,
      "commission_paid_value": 27168.46,
      "net_value": 81505.38
    }
  ],
  "default_sale_flow_rows": [
    {
      "row_slot": 39,
      "installment_count": 1,
      "periodicity": "Sinal",
      "start_month": "2026-03-10",
      "installment_value": 108673.84,
      "percent": 0.04,
      "total_vgv": 108673.84,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    }
  ]
}
```

### Observação de implementação
Os defaults não devem ser montados por heurística. Devem sair da combinação das abas:
- `Tabela Venda - Parcela`
- `Referencias`
- `tbCadastroProduto`
- fórmulas visíveis em `Analise Proposta`

## Endpoint 3, cálculo principal

### `POST /api/v1/scenarios/calculate`
Este é o contrato principal do MVP.

### Regras do endpoint
1. Aceita cenário normal e cenário com permuta.
2. Aceita arrays slotados por linha.
3. Internamente deve normalizar slots ausentes para zero ou vazio, sem reordenar.
4. Deve conseguir devolver tanto resultado resumido quanto trilhas de cálculo para paridade.

### Request schema
```json
{
  "strict_excel_mode": true,
  "parity_trace_requested": true,
  "scenario_mode": "NORMAL | PERMUTA",
  "product_context": {
    "enterprise_name": "string",
    "unit_code": "string",
    "product_unit_key": "string",
    "garage_code": "string | null",
    "private_area_m2": "number",
    "analysis_date": "YYYY-MM-DD",
    "delivery_month": "YYYY-MM-DD",
    "modification_kind": "Não | Decorado (R$/m²) | Facility (R$/m²)",
    "decorated_value_per_m2": "number | null",
    "facility_value_per_m2": "number | null",
    "area_for_modification_m2": "number",
    "prize_enabled": "boolean",
    "fully_invoiced": "boolean",
    "has_permuta": "boolean"
  },
  "commercial_context": {
    "city_sales_manager_name": "string | null",
    "real_estate_name": "string | null",
    "broker_name": "string | null",
    "manager_name": "string | null"
  },
  "commission_context": {
    "primary_commission_label": "string | null",
    "primary_commission_percent": "number | null",
    "prize_commission_label": "string | null",
    "prize_commission_percent": "number | null",
    "secondary_commission_slots": [
      {
        "slot": 1,
        "label": "string | null",
        "percent": "number | null"
      },
      {
        "slot": 2,
        "label": "string | null",
        "percent": "number | null"
      }
    ],
    "parcel_commission_distribution": [
      {
        "distribution_slot": 1,
        "label": "% Sinal | % Parcela 2 | ...",
        "percent": "number | null"
      }
    ],
    "hidden_override": {
      "enabled": "boolean | null",
      "override_percent": "number | null"
    }
  },
  "sale_flow_rows": [
    {
      "row_slot": 39,
      "installment_count": "number | null",
      "periodicity": "string | null",
      "start_month": "YYYY-MM-DD | null",
      "installment_value": "number | null",
      "percent": "number | null",
      "total_vgv": "number | null",
      "adjustment_type": "string | null",
      "notes": "string | null"
    }
  ],
  "exchange_flow_rows": [
    {
      "row_slot": 39,
      "installment_count": "number | null",
      "periodicity": "string | null",
      "start_month": "YYYY-MM-DD | null",
      "installment_value": "number | null",
      "percent": "number | null",
      "total_vgv": "number | null",
      "adjustment_type": "string | null",
      "notes": "string | null"
    }
  ]
}
```

### Normalização obrigatória de slots
A API não deve aceitar apenas um array genérico de parcelas sem slot.  
Ela deve conhecer e preservar os slots 39 a 58 porque:
- a planilha referencia linhas específicas
- parte da comissão depende da ordem das primeiras linhas
- o fluxo mensal depende do casamento entre `Mês início`, periodicidade, contagem e tipo de reajuste
- o trilho de permuta replica a mesma grade

### Exemplo observado, cenário normal
```json
{
  "strict_excel_mode": true,
  "parity_trace_requested": true,
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
      {
        "slot": 1,
        "label": null,
        "percent": null
      },
      {
        "slot": 2,
        "label": null,
        "percent": null
      }
    ]
  },
  "sale_flow_rows": [
    {
      "row_slot": 39,
      "installment_count": 1.0,
      "periodicity": "Sinal",
      "start_month": "2026-03-10",
      "installment_value": 108673.84,
      "percent": 0.04,
      "total_vgv": 108673.84,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 40,
      "installment_count": 1.0,
      "periodicity": "Entrada",
      "start_month": "2026-04-10",
      "installment_value": 81505.37999999999,
      "percent": 0.029999999999999995,
      "total_vgv": 81505.37999999999,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 41,
      "installment_count": 1.0,
      "periodicity": "Entrada",
      "start_month": "2026-05-10",
      "installment_value": 81505.37999999999,
      "percent": 0.029999999999999995,
      "total_vgv": 81505.37999999999,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 42,
      "installment_count": 1.0,
      "periodicity": "Entrada",
      "start_month": "2026-06-10",
      "installment_value": 81505.37999999999,
      "percent": 0.029999999999999995,
      "total_vgv": 81505.37999999999,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 43,
      "installment_count": 14.0,
      "periodicity": "Mensais",
      "start_month": "2026-07-10",
      "installment_value": 38812.085714285706,
      "percent": 0.014285714285714282,
      "total_vgv": 543369.1999999998,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 44,
      "installment_count": 2.0,
      "periodicity": "Semestrais",
      "start_month": "2026-09-10",
      "installment_value": 135842.30000000002,
      "percent": 0.05000000000000001,
      "total_vgv": 271684.60000000003,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 45,
      "installment_count": 1.0,
      "periodicity": "Única",
      "start_month": "2027-03-10",
      "installment_value": 190179.22000000003,
      "percent": 0.07,
      "total_vgv": 190179.22000000003,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 46,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 47,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 48,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 49,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 50,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 51,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 52,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 53,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 54,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 55,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 56,
      "installment_count": 1.0,
      "periodicity": "Financ. Bancário",
      "start_month": "2027-11-10",
      "installment_value": 1358423.0,
      "percent": 0.5,
      "total_vgv": 1358423.0,
      "adjustment_type": "IGPM + 12% a.a",
      "notes": null
    }
  ]
}
```

### Exemplo observado, cenário com permuta
```json
{
  "strict_excel_mode": true,
  "parity_trace_requested": true,
  "scenario_mode": "PERMUTA",
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
    "has_permuta": true
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
      {
        "slot": 1,
        "label": null,
        "percent": null
      },
      {
        "slot": 2,
        "label": null,
        "percent": null
      }
    ]
  },
  "sale_flow_rows": [
    {
      "row_slot": 39,
      "installment_count": 1.0,
      "periodicity": "Sinal",
      "start_month": "2026-03-10",
      "installment_value": 108673.84,
      "percent": 0.04,
      "total_vgv": 108673.84,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 40,
      "installment_count": 1.0,
      "periodicity": "Entrada",
      "start_month": "2026-04-10",
      "installment_value": 81505.37999999999,
      "percent": 0.029999999999999995,
      "total_vgv": 81505.37999999999,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 41,
      "installment_count": 1.0,
      "periodicity": "Entrada",
      "start_month": "2026-05-10",
      "installment_value": 81505.37999999999,
      "percent": 0.029999999999999995,
      "total_vgv": 81505.37999999999,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 42,
      "installment_count": 1.0,
      "periodicity": "Entrada",
      "start_month": "2026-06-10",
      "installment_value": 81505.37999999999,
      "percent": 0.029999999999999995,
      "total_vgv": 81505.37999999999,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 43,
      "installment_count": 14.0,
      "periodicity": "Mensais",
      "start_month": "2026-07-10",
      "installment_value": 38812.085714285706,
      "percent": 0.014285714285714282,
      "total_vgv": 543369.1999999998,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 44,
      "installment_count": 2.0,
      "periodicity": "Semestrais",
      "start_month": "2026-09-10",
      "installment_value": 135842.30000000002,
      "percent": 0.05000000000000001,
      "total_vgv": 271684.60000000003,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 45,
      "installment_count": 1.0,
      "periodicity": "Única",
      "start_month": "2027-03-10",
      "installment_value": 190179.22000000003,
      "percent": 0.07,
      "total_vgv": 190179.22000000003,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 46,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 47,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 48,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 49,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 50,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 51,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 52,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 53,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 54,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 55,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 56,
      "installment_count": 1.0,
      "periodicity": "Financ. Bancário",
      "start_month": "2027-11-10",
      "installment_value": 1358423.0,
      "percent": 0.5,
      "total_vgv": 1358423.0,
      "adjustment_type": "IGPM + 12% a.a",
      "notes": null
    }
  ],
  "exchange_flow_rows": [
    {
      "row_slot": 39,
      "installment_count": 1.0,
      "periodicity": "Sinal",
      "start_month": "2026-03-10",
      "installment_value": 51129.05,
      "percent": 0.07,
      "total_vgv": 51129.05,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 40,
      "installment_count": 1.0,
      "periodicity": "Entrada",
      "start_month": "2026-04-10",
      "installment_value": 43824.9,
      "percent": 0.060000000000000005,
      "total_vgv": 43824.9,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 41,
      "installment_count": 1.0,
      "periodicity": "Entrada",
      "start_month": "2026-05-10",
      "installment_value": 43824.9,
      "percent": 0.060000000000000005,
      "total_vgv": 43824.9,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 42,
      "installment_count": 1.0,
      "periodicity": "Entrada",
      "start_month": "2026-06-10",
      "installment_value": 43824.9,
      "percent": 0.060000000000000005,
      "total_vgv": 43824.9,
      "adjustment_type": "Fixas Irreajustaveis",
      "notes": null
    },
    {
      "row_slot": 43,
      "installment_count": 0.0,
      "periodicity": "Mensais",
      "start_month": "2026-03-10",
      "installment_value": 0.0,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 44,
      "installment_count": 0.0,
      "periodicity": "Semestrais",
      "start_month": "2026-09-10",
      "installment_value": 0.0,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 45,
      "installment_count": 0.0,
      "periodicity": "Única",
      "start_month": "2026-06-10",
      "installment_value": 0.0,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 46,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 47,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 48,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 49,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 50,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 51,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 52,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 53,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 54,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 55,
      "installment_count": null,
      "periodicity": null,
      "start_month": null,
      "installment_value": null,
      "percent": 0.0,
      "total_vgv": 0.0,
      "adjustment_type": "INCC",
      "notes": null
    },
    {
      "row_slot": 56,
      "installment_count": 1.0,
      "periodicity": "Financ. Bancário",
      "start_month": "2026-07-10",
      "installment_value": 547811.25,
      "percent": 0.75,
      "total_vgv": 547811.25,
      "adjustment_type": "IGPM + 12% a.a",
      "notes": null
    }
  ]
}
```

## Response do cálculo

### Response schema
```json
{
  "scenario_mode": "NORMAL | PERMUTA",
  "summary": {
    "normal": {
      "table_total_vgv": "number",
      "proposal_total_vgv": "number",
      "proposal_total_pv": "number",
      "pv_variation_percent": "number",
      "commission_total_percent": "number",
      "commission_total_value": "number",
      "financing_level_ratio": "number | null",
      "pv_status": "string",
      "commission_status": "string",
      "financing_date_status": "string",
      "capture_total_percent": "number | null",
      "risk_level": "Baixo | Médio | Alto"
    },
    "permuta": {
      "exchange_total_vgv": "number",
      "exchange_total_pv": "number",
      "exchange_vpl_variation_percent": "number",
      "exchange_vpl_variation_value": "number",
      "pv_status": "string",
      "commission_status": "string",
      "financing_date_status": "string",
      "capture_total_percent": "number | null",
      "risk_level": "Baixo | Médio | Alto"
    }
  },
  "base_sale_table_rows": [],
  "sale_flow_rows_result": [],
  "exchange_flow_rows_result": [],
  "sale_monthly_flow": [],
  "exchange_monthly_flow": [],
  "indirect_commission": {
    "delivery_month_indirect_commission_value": "number | null",
    "source_cell": "PRC + COORD!O34"
  },
  "warnings": [
    {
      "code": "LATENT_RULE_NOT_MAPPED",
      "message": "string",
      "source_refs": ["Analise Proposta!U41", "Analise Proposta!U42"]
    }
  ],
  "parity_trace": {
    "source_cells": {},
    "source_tables": [],
    "critical_formulas": []
  }
}
```

### Resposta resumida observada, cenário normal
```json
{
  "summary": {
    "normal": {
      "table_total_vgv": 2716846.0,
      "proposal_total_vgv": 2716846.0,
      "proposal_total_pv": 2327435.0465137386,
      "pv_variation_percent": 0.0,
      "commission_total_percent": 0.055,
      "commission_total_value": 149426.53,
      "financing_level_ratio": 1.0,
      "pv_status": "PV Aprovado*",
      "commission_status": "OK",
      "financing_date_status": "OK",
      "capture_total_percent": 0.5,
      "risk_level": "Baixo"
    }
  }
}
```

### Resposta resumida observada, cenário com permuta
```json
{
  "summary": {
    "permuta": {
      "exchange_total_vgv": 730415.0,
      "exchange_total_pv": 605424.7357125155,
      "exchange_vpl_variation_percent": -0.7398747017153582,
      "exchange_vpl_variation_value": -1722010.310801223,
      "pv_status": "PV Reprovado",
      "commission_status": "OK",
      "financing_date_status": "NÃO OK",
      "capture_total_percent": 0.25,
      "risk_level": "Alto"
    }
  }
}
```

## Endpoint 4, persistência mínima do cenário

### `POST /api/v1/scenarios`
Objetivo: salvar um cenário editável sem recalcular regra fora do motor.

### Request
```json
{
  "name": "string",
  "scenario_payload": { },
  "last_calculation_hash": "string",
  "tags": ["string"]
}
```

### Response
```json
{
  "scenario_id": "uuid",
  "name": "string",
  "version": 1,
  "saved_at": "ISO-8601",
  "last_calculation_hash": "string"
}
```

### `GET /api/v1/scenarios/{scenario_id}`
Retorna exatamente o payload persistido, sem mutação semântica.

## Endpoint 5, diagnóstico de paridade

### `POST /api/v1/parity/trace`
Objetivo: comparar payload calculado pelo backend com snapshot esperado da planilha.

### Request
```json
{
  "scenario_payload": { },
  "expected_snapshot": {
    "summary.normal.pv_status": "PV Aprovado*",
    "summary.normal.risk_level": "Baixo",
    "summary.permuta.pv_status": "PV Reprovado"
  }
}
```

### Response
```json
{
  "match": true,
  "differences": [],
  "critical_cells_checked": [
    "Analise Proposta!H85",
    "Analise Proposta!H91",
    "Permuta!H90",
    "Permuta!H96"
  ]
}
```

## Regras de validação de payload

### Bloqueios obrigatórios
- `scenario_mode=PERMUTA` exige `product_context.has_permuta=true`
- `scenario_mode=PERMUTA` exige `exchange_flow_rows`
- `modification_kind=Decorado (R$/m²)` exige `decorated_value_per_m2`
- `modification_kind=Facility (R$/m²)` exige `facility_value_per_m2`
- linhas financeiras só podem usar `Financ. Bancário` ou `Financ. Direto`
- payload com slots duplicados deve falhar
- payload com slot fora de 39 a 58 deve falhar em modo estrito

### Códigos de erro sugeridos
- `REFERENCE_NOT_FOUND`
- `UNIT_NOT_FOUND`
- `INVALID_SLOT`
- `DUPLICATE_SLOT`
- `ENUM_NOT_ALLOWED`
- `PERMUTA_BLOCK_REQUIRED`
- `LATENT_RULE_NOT_MAPPED`
- `PARITY_TRACE_REQUIRED_FOR_BLOCKED_RULE`

## Lacunas mínimas já identificadas que impactam o contrato
1. `Analise Proposta!U41:U42` influencia `N8`, mas não aparece rotulado na leitura visível.
2. `Permuta!P95` tem validação `Sim/Não`, porém não apareceu com rótulo claro nem dependência observável nesta rodada.
3. `Analise Proposta!L12` tem validação com `#REF!` e não pode ser tratada como fonte estável de enum.
4. A metadata da tabela `Tabela` contém `#REF!` em parte das fórmulas de coluna calculada, então o agente deve confiar nas células visíveis e não no XML da tabela para reconstituir a regra.

## Decisão prática para implementação
Até que as lacunas acima sejam abertas:
- o contrato principal segue válido
- `hidden_override` fica opcional
- campos sem rótulo explícito não entram como obrigatórios
- qualquer uso destes campos deve gerar `warning` de paridade
