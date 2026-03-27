# Plano de execução, substituição da Template PV

## Objetivo final
Implementar um serviço web que substitua a planilha **Template PV - Março 26_v4.xlsx**, preservando o comportamento funcional do cálculo atual, incluindo permuta, com testes obrigatórios passando ao final.

## Plataforma de execução
Este plano foi desenhado para execução no **Google Antigravity**, aproveitando o ecossistema já disponível do **antigravity-kit** no projeto, com agentes, skills e workflows customizáveis.

## Fonte de verdade
A única fonte de verdade da regra de negócio é a planilha **Template PV - Março 26_v4.xlsx**.
Mindmaps, requisitos e referências externas podem apoiar nomenclatura e contexto, mas nunca prevalecem sobre o comportamento efetivo do Excel.

## Diretriz transversal de código
Usar **Object Calisthenics** como disciplina preferencial de implementação e revisão, sem dogmatismo cego. Quando uma regra não fizer sentido prático, a exceção deve ser justificada.

## Modelo operacional esperado do agente
Quando receber uma ordem equivalente a **"construa o sistema conforme definido no plano de execução"**, o agente deve operar como **dono operacional faseado do projeto**, e não como executor passivo de tarefas isoladas.

Isso significa que o agente deve:
1. ler este plano e os artefatos de governança operacional
2. localizar a próxima etapa elegível no `project-orchestration/step_catalog.yaml`
3. executar apenas a etapa atual
4. produzir evidências objetivas do que foi feito
5. atualizar o estado do programa em `projects-docs/00-governance/NEXT_CHAT_HANDOFF.md`
6. parar no checkpoint e aguardar validação do usuário
7. após aprovação explícita do usuário, avançar para a próxima etapa elegível sem exigir que o usuário reconstrua o backlog

## Artefatos obrigatórios de governança operacional
O agente deve tratar os seguintes arquivos como parte do protocolo de execução:
- `projects-docs/00-governance/PLAN.md`
- `projects-docs/00-governance/definition_of_done.md`
- `projects-docs/00-governance/execution_policy.md`
- `projects-docs/00-governance/replanning_policy.md`
- `projects-docs/00-governance/NEXT_CHAT_HANDOFF.md`
- `project-orchestration/step_catalog.yaml`

## Definição resumida de concluído
O trabalho só é considerado concluído quando:
1. todo o escopo do MVP estiver implementado
2. venda sem permuta e venda com permuta estiverem cobertas
3. critérios de aceite por feature estiverem atendidos
4. build e testes obrigatórios estiverem passando
5. não houver bloqueio aberto impeditivo
6. a aderência à planilha tiver sido validada nos cenários de paridade definidos
7. as diretrizes técnicas do projeto estiverem respeitadas ou com exceções registradas

## Escopo do MVP
### Entra no MVP
- substituição do uso operacional da planilha por serviço web
- frontend React + Tailwind
- backend Python
- banco de dados MSSQLServer 2022 (informações de conexão via variável de ambiente)
- cálculo do fluxo
- cálculo do PV
- cálculo com permuta
- memória mínima de cálculo
- persistência mínima dos cenários
- testes de paridade com a planilha

### Não entra no MVP, salvo dependência direta da planilha
- CRM completo
- esteira comercial completa
- gestão ampla de workflow jurídico
- gestão do ativo recebido em permuta após a negociação
- integrações externas não necessárias para reproduzir o Excel
- capacidades além do que a planilha já suporta hoje

## Estratégia de execução
O trabalho será conduzido em duas frentes coordenadas.

### Frente A, casca mínima de orquestração
Objetivo: preparar a estrutura mínima para que o Antigravity execute o programa com autonomia controlada.

### Frente B, engenharia reversa da Template PV
Objetivo: transformar o Excel em artefatos executáveis para o projeto.

## Leitura inicial confirmada da planilha
### Abas existentes
- tbCadastroProduto
- Tabela Venda - Parcela
- Referencias
- Analise Proposta
- Permuta
- Fluxo
- PRC + COORD
- Imobs
- Carta Proposta

### Sinais já observados
- Analise Proposta e Permuta concentram entradas manuais
- Fluxo concentra a maior parte das fórmulas
- existem dois trilhos de cálculo: normal e permuta
- várias fórmulas usam `Analise Proposta!N6="Sim"` para alternar o caminho
- nomes definidos como `PctATO`, `PctFin` e `PctMensais` aparecem como percentuais-base da lógica

## Regra de ouro
Nenhum prompt futuro de implementação pode pedir ao agente para adivinhar regra de negócio do cálculo. Toda regra relevante deve ser explicitada a partir da planilha antes de virar etapa de implementação.

## Regra de progressão
O agente não deve esperar que o usuário liste manualmente as próximas features ou refaça o plano de implementação. A progressão deve ser guiada pelo `step_catalog.yaml`, respeitando dependências, checkpoints e regras de replanejamento.
