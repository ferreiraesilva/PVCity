# Plano do modulo administrativo

## Objetivo
Criar a area administrativa necessaria para manter os cadastros vivos do sistema sem dependencia operacional da planilha.

## Motivacao
Os seguintes dados mudam ao longo do tempo e precisam ser operados dentro da aplicacao:
- empreendimentos
- unidades
- precos
- estruturas padrao de pagamento
- imobiliarias parceiras

Como o objetivo do projeto e aposentar o uso operacional do workbook, esses cadastros devem ser mantidos por banco, API e interface administrativa.

## Estrutura de navegacao
O frontend deve ter menu lateral com a secao `Cadastros`.

Entradas minimas:
- `Empreendimentos`
- `Unidades`
- `Fluxos Padrao`
- `Imobiliarias`
- `Importacoes CSV`

Regras adicionais:
- a rolagem principal acontece no workspace da direita, nao no menu lateral em desktop
- cada item acima deve abrir sua propria rotina
- nao usar tabs dentro do workspace para trocar entre CRUDs
- submenus no menu lateral sao o mecanismo preferencial de navegacao interna do backoffice

## CRUDs minimos
### Empreendimentos
Campos minimos:
- nome
- codigo da obra
- SPE
- cidade
- ativo/inativo
- VPL anual
- desconto padrao
- mes de entrega
- data de lancamento
- etapa

### Unidades
Campos minimos:
- empreendimento
- codigo da unidade
- chave produto-unidade
- tipo da unidade
- suites
- garagem
- vagas
- area privativa
- preco base
- status
- captura ideal

### Fluxos Padrao
Campos minimos:
- empreendimento
- `row_slot`
- periodicidade
- quantidade de parcelas
- mes inicial
- valor por parcela
- percentual

### Imobiliarias
Campos minimos:
- nome
- ativo/inativo

## Importacao CSV
Cada grupo de cadastro deve permitir importacao em lote por CSV.

Requisitos minimos:
- validacao de cabecalhos
- preview antes de persistir
- relatorio final com criados, atualizados, ignorados e rejeitados
- rejeicao com motivo por linha invalida
- uso de chave natural para evitar duplicacao cega

## Contratos de API implementados
### Cadastro
- `GET /api/v1/admin/enterprises`
- `POST /api/v1/admin/enterprises`
- `PUT /api/v1/admin/enterprises/{enterprise_id}`
- `DELETE /api/v1/admin/enterprises/{enterprise_id}`

- `GET /api/v1/admin/units`
- `POST /api/v1/admin/units`
- `PUT /api/v1/admin/units/{unit_id}`
- `DELETE /api/v1/admin/units/{unit_id}`

- `GET /api/v1/admin/standard-flows`
- `POST /api/v1/admin/standard-flows`
- `PUT /api/v1/admin/standard-flows/{flow_id}`
- `DELETE /api/v1/admin/standard-flows/{flow_id}`

- `GET /api/v1/admin/real-estate-agencies`
- `POST /api/v1/admin/real-estate-agencies`
- `PUT /api/v1/admin/real-estate-agencies/{agency_id}`
- `DELETE /api/v1/admin/real-estate-agencies/{agency_id}`

### Importacao
- `POST /api/v1/admin/import/enterprises/preview`
- `POST /api/v1/admin/import/enterprises/commit`
- `POST /api/v1/admin/import/units/preview`
- `POST /api/v1/admin/import/units/commit`
- `POST /api/v1/admin/import/standard-flows/preview`
- `POST /api/v1/admin/import/standard-flows/commit`
- `POST /api/v1/admin/import/real-estate-agencies/preview`
- `POST /api/v1/admin/import/real-estate-agencies/commit`

## Regra de separacao
- workbook: engenharia reversa, paridade e recalculo comparativo
- banco + backend + frontend administrativo: operacao oficial do sistema

## Criterio de pronto do modulo
O modulo administrativo so pode ser considerado pronto quando:
- os CRUDs minimos existirem
- a navegacao lateral existir
- a importacao CSV existir para os grupos criticos
- o calculo passar a depender apenas dos cadastros operacionais

## Estado atual
Implementado nesta rodada:
- router FastAPI `/api/v1/admin` com CRUD para empreendimentos, unidades, fluxos padrao e imobiliarias
- importacao CSV com `preview` e `commit`
- menu lateral no frontend com submenu para cada rotina administrativa
- telas operacionais separadas para listagem, criacao, edicao, exclusao e importacao

Ponto de atencao:
- o backoffice ja opera pelos modelos do banco, mas a base ainda precisa ser populada e validada com carga real
