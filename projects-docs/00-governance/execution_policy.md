# Execution Policy, condução autônoma faseada

## Objetivo
Transformar o plano em protocolo operacional para que o agente conduza o projeto por etapas, sem depender de o usuário reconstruir o backlog a cada ciclo.

## Comando de entrada esperado
Uma ordem equivalente a abaixo deve ser suficiente para iniciar ou retomar o programa:

> construa o sistema conforme definido no plano de execução

Ao receber esse comando, o agente deve entender que:
- o plano já existe
- a condução é faseada
- o backlog deve ser lido do `step_catalog.yaml`
- o usuário atua como cliente e aprovador de checkpoints
- o agente atua como dono operacional da execução dentro do escopo definido

## Artefatos obrigatórios de leitura antes de agir
O agente deve ler, nesta ordem lógica:
1. `projects-docs/00-governance/PLAN.md`
2. `projects-docs/00-governance/definition_of_done.md`
3. `projects-docs/00-governance/execution_policy.md`
4. `projects-docs/00-governance/replanning_policy.md`
5. `projects-docs/00-governance/NEXT_CHAT_HANDOFF.md`
6. `project-orchestration/step_catalog.yaml`

Quando a etapa exigir, o agente deve então ler os artefatos específicos listados em `read_artifacts`.

## Papel do agente
O agente é responsável por:
- identificar a próxima etapa elegível
- executar a etapa atual sem pedir ao usuário a decomposição do backlog
- respeitar dependências, restrições e critérios de aceite
- registrar checkpoint ao final da etapa
- sugerir a próxima etapa elegível
- aguardar aprovação do usuário no checkpoint

O agente não deve:
- pedir ao usuário para lembrar todas as próximas features
- reabrir decisões já fechadas
- inventar regra de negócio para preencher lacunas do Excel
- avançar para múltiplas etapas sem checkpoint, salvo instrução explícita do usuário

## Regra de escolha da próxima etapa
A próxima etapa elegível é a primeira etapa do `step_catalog.yaml` que simultaneamente:
1. tenha todas as dependências satisfeitas
2. ainda não esteja marcada como `done` no checkpoint vigente
3. não esteja bloqueada por regra de replanejamento
4. seja compatível com o escopo atual já aprovado

Se mais de uma etapa estiver elegível, o agente deve priorizar:
1. `critical`
2. menor distância para execução real do MVP
3. fechamento de lacuna que bloqueia implementação ou paridade

## Regra de execução por etapa
Para cada etapa, o agente deve seguir este ciclo:
1. confirmar o escopo exato da etapa
2. ler os artefatos obrigatórios
3. executar a etapa
4. produzir ou atualizar artefatos
5. validar contra `done_when` e `evidence_required`
6. registrar checkpoint em `NEXT_CHAT_HANDOFF.md`
7. parar e devolver a bola ao usuário

## Regra de checkpoint obrigatório
Toda etapa deve terminar em checkpoint. O agente deve devolver ao usuário, de forma objetiva:
- etapa executada
- objetivo da etapa
- artefatos lidos
- artefatos criados ou alterados
- evidências de conclusão
- lacunas abertas ou bloqueios
- próxima etapa elegível sugerida pelo plano
- decisão esperada do usuário: aprovar, ajustar ou bloquear

## Regra de espera
Após um checkpoint, o agente deve aguardar:
- aprovação do usuário para avançar
- solicitação de ajuste na etapa atual
- desbloqueio de questão material

Sem uma dessas três condições, o agente não deve presumir que pode pular para a próxima etapa.

## Regra para continuidade após aprovação
Após aprovação explícita do usuário, o agente deve:
1. atualizar o estado da etapa anterior para `done`
2. selecionar a próxima etapa elegível no `step_catalog.yaml`
3. iniciar a execução da nova etapa sem exigir que o usuário reconstrua o plano

## Regra de aderência ao Excel
Sempre que a etapa tocar regra de negócio, contrato, fluxo, comissão, PV, permuta ou paridade:
- a Template PV continua sendo a fonte de verdade
- abstração elegante nunca prevalece sobre comportamento observado do workbook
- `row_slot` deve ser preservado quando isso for parte da lógica do Excel
- regra não observada deve virar lacuna ou bloqueio, não implementação presumida

## Regra para artefatos de estado
`projects-docs/00-governance/NEXT_CHAT_HANDOFF.md` deixa de ser apenas memória conversacional e passa a ser o **estado resumido do programa**.

Ele deve sempre conter:
- situação atual
- últimas etapas concluídas
- etapa em revisão
- bloqueios e lacunas abertas
- próxima etapa elegível sugerida
- lista canônica dos artefatos relevantes do programa

## Regra para implementação
Quando a etapa for de código, o agente deve:
- implementar apenas o que a etapa cobre
- não abrir escopo lateral
- incluir evidência executável, como testes ou comando de validação
- registrar claramente o que ainda não foi feito

## Regra para documentação
Quando a etapa for documental, o agente deve:
- produzir documento pronto para uso no projeto
- reduzir ambiguidade operacional
- melhorar capacidade de execução autônoma do passo seguinte

## Falhas de execução
Constituem falha de execução do agente:
- exigir que o usuário remonte o backlog que já está no plano
- avançar sem checkpoint
- declarar pronto sem evidência
- tratar permuta como opcional
- ignorar uma lacuna material do Excel e seguir mesmo assim
