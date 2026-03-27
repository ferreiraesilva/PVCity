# Replanning Policy, bloqueios, lacunas e retorno controlado

## Objetivo
Definir como o agente deve reagir quando encontrar ambiguidade, lacuna, contradição ou impedimento, sem perder aderência ao plano e sem inventar regra.

## Quando replanejar
O agente deve replanejar quando ocorrer qualquer uma das situações abaixo:
- uma etapa depende de artefato que não existe
- uma regra central do Excel não está suficientemente evidenciada
- há contradição entre artefatos do projeto
- a implementação falha em paridade de forma estrutural
- um bloco de trabalho originalmente previsto não cabe mais na etapa atual
- um arquivo está no lugar errado e isso cria ambiguidade operacional para os próximos passos

## Quando não replanejar
O agente não deve abrir replanejamento por:
- preferência estética de modelagem
- vontade de trocar stack já definida
- oportunidade de melhoria sem impacto na aderência ao Excel
- desejo de antecipar feature fora do escopo do MVP

## Tipos de situação e reação esperada
### 1. Lacuna documental não impeditiva
Exemplo: campo latente mapeado, mas ainda não crítico para a etapa atual.

Ação esperada:
- registrar em documento de gaps
- seguir com warning
- não bloquear a etapa atual

### 2. Lacuna documental impeditiva
Exemplo: fórmula central do cálculo não suficientemente aberta para implementar ou validar.

Ação esperada:
- parar a execução da etapa atual
- abrir ou atualizar artefato de gap
- propor etapa corretiva mínima
- retornar checkpoint ao usuário

### 3. Divergência de implementação versus paridade
Exemplo: cálculo roda, mas diverge do Excel em campo crítico.

Ação esperada:
- não mascarar a divergência
- regredir logicamente para a etapa anterior relevante
- abrir evidência da divergência
- tratar a correção como prioridade antes de avançar

### 4. Contradição entre artefatos do projeto
Exemplo: caminho em `PLAN.md` diverge do `step_catalog.yaml`.

Ação esperada:
- corrigir a camada de governança primeiro
- congelar um caminho canônico
- registrar no checkpoint que houve saneamento estrutural

## Política de gaps
Toda lacuna aberta deve informar:
- qual é a evidência
- por que a lacuna existe
- qual o impacto prático
- se ela bloqueia ou não a próxima etapa
- qual o tratamento adotado nesta rodada

## Política de retorno de etapa
Se uma etapa falhar por causa de paridade, contrato ou regra central, o agente deve voltar para a etapa mais próxima capaz de corrigir a causa raiz, e não só remendar a saída.

Ordem típica de retorno:
1. implementação
2. contrato de API
3. engenharia reversa da regra afetada
4. governança, apenas se o problema for estrutural de orquestração

## Política para caminhos e estrutura
Quando existir duplicidade ou inconsistência de caminhos, o agente deve:
1. eleger um caminho canônico
2. atualizar artefatos de governança para esse caminho
3. orientar remoção das cópias legadas se existirem

## Política para etapas corretivas
Etapas corretivas devem ser:
- mínimas
- rastreáveis
- alinhadas ao plano existente
- focadas na causa raiz

## Saída obrigatória de replanejamento
Quando houver replanejamento, o checkpoint ao usuário deve informar:
- o que disparou o replanejamento
- qual etapa foi interrompida
- qual etapa corretiva foi aberta ou reativada
- o que continua bloqueado
- qual decisão o usuário precisa tomar, se houver
