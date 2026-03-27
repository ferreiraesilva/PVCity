# Definition of Done, MVP Template PV

## Objetivo
Definir quando uma etapa individual e quando o programa inteiro podem ser considerados prontos, sem depender de interpretação livre do agente.

## Definition of Done global do programa
O programa só pode ser marcado como concluído quando todos os itens abaixo forem verdadeiros:
1. o serviço web substitui a operação principal da Template PV no escopo do MVP
2. cálculo sem permuta e cálculo com permuta funcionam
3. backend Python e frontend React + Tailwind estão implementados no escopo mínimo necessário
4. persistência mínima de cenários existe
5. testes obrigatórios passam
6. cenários de paridade definidos contra o Excel passam
7. não existe bloqueio aberto impeditivo
8. warnings latentes conhecidos estão tratados ou registrados
9. a implementação respeita as decisões já congeladas no plano

## Definition of Done por etapa
Uma etapa do `step_catalog.yaml` só pode ser considerada concluída quando:
1. o objetivo da etapa foi entregue
2. os artefatos esperados da etapa existem ou foram atualizados
3. as evidências exigidas pela etapa foram produzidas
4. os critérios `done_when` da etapa foram atendidos
5. não houve violação de regra inegociável
6. o checkpoint da etapa foi registrado em `projects-docs/00-governance/NEXT_CHAT_HANDOFF.md`
7. a etapa está em estado `review_pending` ou `done`, nunca em limbo implícito

## Definition of Done para etapas de documentação
Além das regras gerais, etapas de documentação devem:
- estar coerentes com a fonte de verdade
- evitar reabrir decisão fechada
- deixar claro o que é evidência e o que é hipótese
- registrar lacunas mínimas sem expandir escopo desnecessariamente

## Definition of Done para etapas de implementação
Além das regras gerais, etapas de implementação devem:
- produzir código executável
- respeitar o contrato de API vigente
- preservar `row_slot` quando aplicável
- suportar permuta quando a etapa tocar o motor principal
- incluir testes compatíveis com o escopo da etapa
- registrar limitações reais em vez de mascarar incompletude

## Definition of Done para etapas de paridade
Além das regras gerais, etapas de paridade devem:
- comparar contra a Template PV
- usar tolerâncias formalizadas
- destacar divergências por campo crítico
- reprovar imediatamente em caso de divergência estrutural, de slot ou de status crítico

## Evidência mínima obrigatória em cada checkpoint
Cada checkpoint deve informar, no mínimo:
- o que foi lido
- o que foi alterado
- o que foi provado
- o que ainda está aberto
- qual é a próxima etapa elegível sugerida pelo plano

## O que não conta como concluído
Os itens abaixo não autorizam marcar etapa ou programa como concluídos:
- só existir texto sem artefato final utilizável
- só existir scaffold sem aderência ao contrato ou ao Excel
- testes ausentes ou ignorados
- paridade sem evidência objetiva
- bloqueio relevante escondido como observação menor
- avanço para a próxima etapa sem checkpoint claro
