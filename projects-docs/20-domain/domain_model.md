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

## Regra de ouro
Nenhuma regra relevante de comissão, cronograma ou valor presente deve morar no frontend.
