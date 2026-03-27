# Estado resumido do programa — Handoff Operacional
> **Este arquivo é a única fonte de estado do programa entre sessões.**
> O agente deve lê-lo como primeira ação antes de qualquer pergunta ao usuário.

---

## 🟢 Ponto de Retomada
O backend Python/FastAPI está **100% implementado e testado**.
A próxima etapa é **IMPL-02: Frontend React + Tailwind CSS**.

---

## Regras Inegociáveis (não reabrir)
- A única fonte de verdade de regras de negócio é `projects-docs/references/source-of-truth/Template PV - Março 26_v4.xlsx`
- Permuta é escopo obrigatório do MVP
- Object Calisthenics: sem primitivos expostos, sem `else` após `return`, sem abreviações
- Código e comentários em inglês
- O banco de dados (MSSQLServer 2022) será criado e populado em fase separada futura
- Não reinventar regras de negócio — se houver lacuna, aplicar `replanning_policy.md`

## Estratégia de Modelos
| Tarefa | Modelo |
|---|---|
| Frontend React + Tailwind (IMPL-02) | **Gemini 1.5 Flash** |
| Core de cálculo / lógica financeira | **Claude 3.5 Sonnet** |
| Banco de dados e integrações | **Claude 3.5 Sonnet** |

---

## Verificação Imediata — Execute Antes de Prosseguir
```bash
cd c:\Projetos\PVCity
python -m pytest tests/ -q
# Esperado: 20 passed in ~0.16s
```

Se os 20 testes passarem, o backend está íntegro. Pode iniciar IMPL-02 diretamente.

---

## Arquitetura de Pastas Atual
```
c:\Projetos\PVCity\
  backend/
    app/
      main.py                           # FastAPI - 5 routers
      core/config.py                    # MSSQL env vars
      schemas/scenarios.py              # Pydantic contracts
      api/v1/endpoints/
        scenarios.py                    # POST /api/v1/scenarios/calculate
        scenario_store.py               # POST + GET /api/v1/scenarios
        bootstrap.py                    # GET /api/v1/bootstrap/reference-data
        products.py                     # GET /api/v1/products/{e}/units/{u}/defaults
        parity.py                       # POST /api/v1/parity/trace
      services/
        domain/
          proposal.py                   # ProposalSlot, ProposalRows, MonthOffset
          rates.py                      # FinancialRates (J6, J7, J8)
          cash_flow.py                  # MonthlyCashFlowEvent, CashFlowSummary
        monthly_schedule_engine.py      # ENGINE PRINCIPAL - mirrors tbFluxo LET+SUMPRODUCT
        scenario_builder.py             # ScenarioBuilder, normalizers
        commission_calculator.py        # CommissionBaseCalculator (N8:N12, R35:R36)
        summary_engine.py               # SummaryEngine (H85:H91, H88:H96)
        parity_guard.py                 # ParityGuardService, tolerâncias
        payload_validator.py            # 4 regras de validação do contrato
    requirements.txt
  tests/
    parity/test_golden_cases.py         # 20 testes
  pyproject.toml                        # pytest pythonpath config
  projects-docs/
    00-governance/
      PLAN.md, definition_of_done.md, execution_policy.md,
      replanning_policy.md, NEXT_CHAT_HANDOFF.md (este arquivo)
    10-excel-reverse-engineering/       # Todos os mapeamentos do Excel
    20-domain/api_contracts_draft.md    # Contratos de API detalhados
    30-architecture/
      golden_test_cases.md              # GT-001 e GT-002
      parity_rules.md                   # Tolerâncias e regras de paridade
    references/source-of-truth/         # Template PV - Março 26_v4.xlsx
  project-orchestration/step_catalog.yaml
  .agent/                               # antigravity-kit (não modificar)
```

---

## Endpoints Backend Disponíveis

| Método | Rota | Status |
|---|---|---|
| POST | `/api/v1/scenarios/calculate` | ✅ Motor real |
| POST | `/api/v1/scenarios` | ✅ in-memory (TODO:DB) |
| GET | `/api/v1/scenarios/{id}` | ✅ in-memory (TODO:DB) |
| GET | `/api/v1/bootstrap/reference-data` | ✅ mocked (TODO:DB) |
| GET | `/api/v1/products/{e}/units/{u}/defaults` | ✅ mocked (TODO:DB) |
| POST | `/api/v1/parity/trace` | ✅ |

**Como rodar o backend:**
```bash
cd c:\Projetos\PVCity\backend
uvicorn app.main:app --reload --port 8000
# Swagger em: http://localhost:8000/api/v1/openapi.json
```

---

## O que o TODO:DB significa
Todos os endpoints marcados `TODO:DB` funcionam com dados mockados do Excel.
Quando o banco for criado (fase futura), basta substituir os mocks por leituras SQLAlchemy/pyodbc.
As constantes `PLACEHOLDER_VPL_RATE = 0.10` e `PLACEHOLDER_PRC_COORD_O34 = 100523.302`
no arquivo `scenarios.py` também precisarão vir do banco.

---

## Próxima Etapa: IMPL-02 — Frontend React + Tailwind

**Modelo recomendado: Gemini 1.5 Flash**

### Escopo do Frontend
1. Scaffold Vite + React + Tailwind CSS
2. Página principal: formulário de Proposta (slots 39-58 + contexto do produto)
3. Integração com `GET /bootstrap/reference-data` para popular selects
4. Integração com `POST /scenarios/calculate` para exibir resultado
5. Exibição do Summary (pv_status, risk_level, commission, etc.)
6. Fluxo mensal em tabela ou gráfico
7. Suporte a cenário NORMAL e PERMUTA

### Referências de design para o frontend
- `projects-docs/20-domain/api_contracts_draft.md` — estrutura de dados
- `projects-docs/30-architecture/golden_test_cases.md` — valores esperados na UI

---

## Artefatos de Governança para Leitura Obrigatória (se necessário)
1. `projects-docs/00-governance/PLAN.md`
2. `projects-docs/00-governance/definition_of_done.md`
3. `projects-docs/00-governance/execution_policy.md`
4. `projects-docs/00-governance/replanning_policy.md`
5. `project-orchestration/step_catalog.yaml`
