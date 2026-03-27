# Estado resumido do programa, handoff operacional

## Papel deste arquivo
Este arquivo é o estado resumido do programa para continuidade entre janelas. Ele não é apenas memória de conversa. Ele informa ao agente onde o programa está, o que já foi consolidado, o que está em revisão e qual é a próxima etapa elegível sugerida.

## Situação atual
O usuário confirmou que **todo o processo de Discovery (Engenharia Reversa)** já foi conduzido em sessões passadas. Todos os contratos de dados e lógicas estão formalizados e homologados sob os arquivos principais (ex: `api_contracts_draft.md` e `domain_model.md`). As ações recentes de geração de novos Mapeamentos (`fluxo_formula_map.md` e `fluxo_bucket_rules.md`) foram apenas fechamentos burocráticos para alinhar os exigíveis fixos previstos no `step_catalog.yaml`.

## Decisões congeladas
- **Fase de Discovery está oficialmente Encerrada.** Nenhuma nova documentação de mapeamento deverá ser iniciada salvo problemas não mapeados surgirem durante a construção de código.
- MVP = substituir a Template PV por serviço web
- Frontend = React + Tailwind
- Backend = Python + FastAPI integrado ao banco de dados MSSQLServer 2022 (base `city`, usuário `city_apping`, senha via variável de ambiente)
- Permuta é escopo obrigatório
- Object Calisthenics e código em inglês obrigatórios.

## Artefatos governantes do programa
- `projects-docs/00-governance/PLAN.md`
- `project-orchestration/step_catalog.yaml`

## Etapa em revisão nesta rodada
`DISCOVERY - CONSOLIDATION` - Ajuste de governança assumindo que a parte teórica já foi exaurida através dos contatos passados.

## Próxima etapa elegível sugerida
**`TEST-01` e `IMPL-01`** - Mão na massa. Fase inicial da estrutura de engenharia de software real (Backend e Base Test-Driven guiados para bater os mesmos centavos mapeados no `golden_test_cases.md`).

## Checkpoint desta rodada
### O que foi consolidado
- Fim da ambiguidade teórica: Todas as minúcias mapeadas.
- Todas as passagens de premissa `EXCEL-*`, `DOMAIN-01` e `API-01` marcadas e aceitas como finalizadas.

### O que ainda está aberto
- Início do scaffold arquitetural real e programação dos mocks estritos (Escrita de Código Python, Pastas do projeto, Pytest/Unit Tests baseados no Excel).

## Instrução para a próxima janela
Qualquer ação de "Executar programa" deve imediatamente inicializar as ferramentas de edição de código e montar a suíte de Testes (TDD/Paridade) alinhada à etapa `TEST-01`, ou já disparar serviços backend caso os testes já tenham infra. O Agente deve deixar o chapéu de "Analista de Excel" e assumir o de Engenheiro de Software Fullstack e Testes.
