# Domínio mínimo do MVP

## Princípio de modelagem
O sistema deve ser modelado por cenário, não por tela.

## Glossário
- AnalysisScenario: cenário comercial completo
- ProposalScenario: proposta financeira concreta, normal ou com permuta
- ProposalLine: cada linha parametrizada da grade da proposta
- TradeInAsset: bem entregue como parte do pagamento
- MonthlyCashFlowEvent: ocorrência mensal materializada a partir da proposta ou da tabela
- CommissionDistribution: comissão distribuída por papel comercial e por parcela
- PresentValueSnapshot: resultado consolidado do desconto a valor presente
- CalculationTrace: memória mínima do cálculo
- Enterprise: empreendimento comercializado
- Unit: unidade imobiliária de um empreendimento
- UnitStandardFlow: tabela padrão de pagamento vinculada ao empreendimento
- RealEstateAgency: imobiliária parceira disponível para operação
- RuntimeDefaults: parâmetros operacionais padrão do sistema, independentes do workbook

## Serviços de domínio obrigatórios
- ScenarioBuilder
- ProposalLineNormalizer
- MonthlyScheduleEngine
- CashFlowBucketClassifier
- CommissionBaseCalculator
- CommissionAllocationEngine
- IndirectCommissionEventFactory
- PresentValueEngine
- ScenarioComparisonService
- ParityGuardService

## Módulo administrativo obrigatório
Para aposentar o uso operacional da planilha, o sistema precisa de um módulo administrativo para manutenção dos cadastros vivos do negócio.

Capacidades mínimas:
- CRUD de empreendimentos
- CRUD de unidades
- CRUD da estrutura padrão de pagamento por empreendimento
- CRUD de imobiliárias
- importação CSV para carga e atualização em lote

Regra de separação:
- workbook: engenharia reversa, paridade e recálculo comparativo
- banco + backend: operação oficial do sistema

## Regra de ouro
Nenhuma regra relevante de comissão, cronograma ou valor presente deve morar no frontend.
