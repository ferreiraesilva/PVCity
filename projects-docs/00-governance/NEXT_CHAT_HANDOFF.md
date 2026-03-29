# Estado resumido do programa - Handoff operacional
> Este arquivo e a unica fonte de estado do programa entre sessoes.
> O agente deve le-lo antes de retomar o trabalho.

---

## Ponto de retomada
O sistema ja tem:
- fluxo principal de simulacao em React + Tailwind
- backend FastAPI com calculo operacional
- separacao explicita entre workbook de paridade e runtime oficial
- backoffice inicial para manutencao de cadastros operacionais

A proxima frente prioritaria e consolidar a operacao real do banco:
- popular e validar dados reais
- endurecer contratos do modulo administrativo
- fechar a paridade financeira restante contra o workbook

---

## Regras inegociaveis
- A planilha em `projects-docs/references/source-of-truth/Template PV - Marco 26_v4.xlsx` e fonte de verdade para engenharia reversa
- A planilha nao pode ser dependencia operacional do produto final
- Workbook serve apenas para paridade, investigacao e recalculo comparativo
- Permuta e escopo obrigatorio do MVP
- Em arquivos XLSX:
  1. nunca assumir recalculo via openpyxl
  2. executar `python .agent/scripts/recalc_xlsx.py <arquivo> <saida>` antes de confiar em resultados finais
  3. se LibreOffice nao estiver disponivel, registrar explicitamente que a analise e estrutural
  4. distinguir sempre recalculo real vs inspecao logica

---

## Estado arquitetural atual
### Backend
- `backend/app/api/v1/endpoints/scenarios.py`: calculo principal
- `backend/app/api/v1/endpoints/bootstrap.py`: referencia operacional vinda do banco
- `backend/app/api/v1/endpoints/products.py`: defaults da unidade a partir do banco
- `backend/app/api/v1/endpoints/admin.py`: CRUD e importacao CSV do backoffice
- `backend/app/services/database_reference_service.py`: fonte operacional do runtime
- `backend/app/services/workbook_reference_service.py`: uso restrito a engenharia reversa/paridade
- `backend/app/services/admin_service.py`: CRUDs e importacao CSV

### Frontend
- `frontend/src/App.jsx`: shell com menu lateral
- `frontend/src/components/simulation/SimulationWorkspace.jsx`: simulador
- `frontend/src/components/admin/AdminWorkspace.jsx`: backoffice inicial

### Documentacao
- `projects-docs/20-domain/admin_backoffice_plan.md`: contrato do modulo administrativo
- `projects-docs/20-domain/domain_model.md`: entidades operacionais
- `projects-docs/30-architecture/parity_rules.md`: regras de paridade

---

## Endpoints disponiveis
| Metodo | Rota | Status |
|---|---|---|
| GET | `/api/v1/bootstrap/reference-data` | operacional |
| GET | `/api/v1/products/{enterprise_name}/units/{unit_code}/defaults` | operacional |
| POST | `/api/v1/scenarios/calculate` | operacional |
| POST | `/api/v1/parity/trace` | paridade |
| GET/POST/PUT/DELETE | `/api/v1/admin/enterprises` | operacional |
| GET/POST/PUT/DELETE | `/api/v1/admin/units` | operacional |
| GET/POST/PUT/DELETE | `/api/v1/admin/standard-flows` | operacional |
| GET/POST/PUT/DELETE | `/api/v1/admin/real-estate-agencies` | operacional |
| POST | `/api/v1/admin/import/{resource}/preview` | operacional |
| POST | `/api/v1/admin/import/{resource}/commit` | operacional |

---

## Validacao recente
- `python -m py_compile backend/app/main.py backend/app/api/v1/endpoints/admin.py backend/app/services/admin_service.py backend/app/schemas/admin.py`
- `python -c "from app.main import app"` com `PYTHONPATH=backend`
- `npm run build` em `frontend/`

---

## Proximas etapas prioritarias
1. Popular a base com dados reais de empreendimentos, unidades, fluxos e imobiliarias.
2. Adicionar validacoes de negocio mais estritas no backoffice:
   - unicidade e consistencia de slots
   - relatorios de importacao mais ricos
   - filtros e busca nas listagens
3. Fechar a paridade financeira restante no calculo:
   - comissao indireta
   - detalhes finos de `commission_status`
4. Se necessario, criar migracoes adicionais e seeds para carga inicial.
