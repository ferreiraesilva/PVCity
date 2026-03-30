import { useEffect, useMemo, useState } from 'react';
import { ArrowRightLeft, Calculator } from 'lucide-react';

import { Card } from '../shared/Card';
import { Button } from '../shared/Button';
import { Input } from '../shared/Input';
import { Select } from '../shared/Select';
import { ProposalForm } from '../proposal/ProposalForm';
import { SummaryCard } from '../results/SummaryCard';
import { EconomicIndicators } from '../results/EconomicIndicators';
import { useScenarioState } from '../../hooks/useScenarioState';
import { services } from '../../api/services';
import { formatDatePTBR } from '../../utils/dateUtils';


const YES_NO_OPTIONS = [
  { label: 'Sim', value: 'true' },
  { label: 'Não', value: 'false' },
];


export function SimulationWorkspace({ referenceData }) {
  const state = useScenarioState();
  const [result, setResult] = useState(null);
  const [defaultsLoading, setDefaultsLoading] = useState(false);
  const [calculating, setCalculating] = useState(false);
  const [screenError, setScreenError] = useState('');

  const isPermuta = state.scenarioMode === 'PERMUTA';
  const canCalculate = Boolean(
    state.productContext.enterprise_name &&
      state.productContext.unit_code &&
      state.productContext.analysis_date &&
      !defaultsLoading
  );

  useEffect(() => {
    state.updateProductContext('has_permuta', isPermuta);
  }, [isPermuta]);

  const enterpriseOptions = useMemo(() => {
    const seen = new Set();
    return (referenceData?.products || [])
      .filter((product) => {
        if (seen.has(product.enterprise_name)) {
          return false;
        }
        seen.add(product.enterprise_name);
        return true;
      })
      .map((product) => ({
        value: product.enterprise_name,
        label: product.enterprise_name,
      }));
  }, [referenceData]);

  const unitOptions = useMemo(() => {
    return (referenceData?.unit_lookup_keys || [])
      .filter((unit) => unit.enterprise_name === state.productContext.enterprise_name)
      .map((unit) => ({
        value: unit.unit_code,
        label: `${unit.unit_code} • ${unit.status || 'Sem status'}`,
      }));
  }, [referenceData, state.productContext.enterprise_name]);

  const selectedUnit = useMemo(() => {
    return (referenceData?.unit_lookup_keys || []).find(
      (unit) =>
        unit.enterprise_name === state.productContext.enterprise_name &&
        unit.unit_code === state.productContext.unit_code
    );
  }, [referenceData, state.productContext.enterprise_name, state.productContext.unit_code]);

  const summary = isPermuta ? result?.summary?.permuta : result?.summary?.normal;
  const monthlyFlow = isPermuta ? result?.exchange_monthly_flow : result?.sale_monthly_flow;

  const handleEnterpriseChange = (enterpriseName) => {
    setResult(null);
    state.clearUnitSelection(enterpriseName);
  };

  const handleUnitChange = async (unitCode) => {
    if (!state.productContext.enterprise_name || !unitCode) {
      return;
    }

    try {
      setDefaultsLoading(true);
      setScreenError('');
      setResult(null);
      const defaults = await services.getUnitDefaults(
        state.productContext.enterprise_name,
        unitCode
      );
      state.applyUnitDefaults(defaults, isPermuta);
    } catch (error) {
      const message = error.code === 'ECONNABORTED'
        ? 'Erro operacional: Timeout. O fluxo padrão demorou muito a carregar (10s).'
        : 'Não foi possível carregar o fluxo padrão da unidade selecionada.';
      setScreenError(message);
      state.clearUnitSelection(state.productContext.enterprise_name);
    } finally {
      setDefaultsLoading(false);
    }
  };

  const handleCalculate = async () => {
    if (!canCalculate) {
      return;
    }

    try {
      setCalculating(true);
      setScreenError('');
      const payload = {
        strict_excel_mode: true,
        parity_trace_requested: true,
        scenario_mode: state.scenarioMode,
        product_context: state.productContext,
        commercial_context: state.commercialContext,
        commission_context: state.commissionContext,
        financial_rates: state.financialRates,
        sale_flow_rows: state.saleFlowRows.filter(
          (row) => row.installment_count || row.installment_value || row.total_vgv
        ),
        exchange_flow_rows: state.exchangeFlowRows.filter(
          (row) => row.installment_count || row.installment_value || row.total_vgv
        ),
        standard_flow_rows: state.standardFlowRows.filter(
          (row) => row.installment_count || row.installment_value || row.total_vgv
        ),
      };
      const response = await services.calculateScenario(payload);
      setResult(response);
    } catch (error) {
      const message = error.code === 'ECONNABORTED'
        ? 'Erro operacional: Timeout. O cálculo de PV demorou muito (10s).'
        : 'Falha ao calcular o cenário.';
      setScreenError(message);
    } finally {
      setCalculating(false);
    }
  };

  return (
    <main className="grid grid-cols-1 gap-6 xl:grid-cols-12">
      <section className="xl:col-span-8">
        <div className="flex flex-col gap-6">
          <Card>
            <h2 className="mb-4 text-lg font-semibold text-city-blue-dark">
              Contexto da análise
            </h2>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <Select
                label="Empreendimento"
                value={state.productContext.enterprise_name}
                options={enterpriseOptions}
                onChange={(event) => handleEnterpriseChange(event.target.value)}
                disabled={!referenceData}
              />
              <Select
                label="Unidade"
                value={state.productContext.unit_code}
                options={unitOptions}
                onChange={(event) => handleUnitChange(event.target.value)}
                disabled={!state.productContext.enterprise_name || defaultsLoading}
              />
              <Input
                label="Data-base"
                type="date"
                value={state.productContext.analysis_date}
                onChange={(event) =>
                  state.updateProductContext('analysis_date', event.target.value)
                }
                disabled={!state.productContext.unit_code}
              />
            </div>

            <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
              <Select
                label="Prêmio?"
                value={state.productContext.prize_enabled ? 'true' : 'false'}
                options={YES_NO_OPTIONS}
                onChange={(event) =>
                  state.updateProductContext('prize_enabled', event.target.value === 'true')
                }
                disabled={!state.productContext.unit_code}
              />
              <Select
                label="Toda Faturada?"
                value={state.productContext.fully_invoiced ? 'true' : 'false'}
                options={YES_NO_OPTIONS}
                onChange={(event) =>
                  state.updateProductContext('fully_invoiced', event.target.value === 'true')
                }
                disabled={!state.productContext.unit_code}
              />
            </div>

            <div className="mt-4 grid grid-cols-1 gap-4 text-sm text-text-muted md:grid-cols-4">
              <div>
                <div className="font-medium text-text-main">Status da unidade</div>
                <div>{selectedUnit?.status || '--'}</div>
              </div>
              <div>
                <div className="font-medium text-text-main">Preço base</div>
                <div>
                  {selectedUnit
                    ? new Intl.NumberFormat('pt-BR', {
                        style: 'currency',
                        currency: 'BRL',
                      }).format(selectedUnit.base_price || 0)
                    : '--'}
                </div>
              </div>
              <div>
                <div className="font-medium text-text-main">Área privativa</div>
                <div>
                  {selectedUnit?.private_area_m2
                    ? `${selectedUnit.private_area_m2.toFixed(2)} m²`
                    : '--'}
                </div>
              </div>
              <div>
                <div className="font-medium text-text-main">Entrega</div>
                <div className="font-mono">{formatDatePTBR(state.productContext.delivery_month)}</div>
              </div>
            </div>

            {screenError ? (
              <div className="mt-4 rounded-lg border border-danger-red/30 bg-danger-red/10 px-4 py-3 text-sm text-danger-red">
                {screenError}
              </div>
            ) : null}
          </Card>

          <ProposalForm
            title="Fluxo padrão (Referência)"
            rows={state.standardFlowRows}
            onRowChange={() => {}}
            readOnly={true}
            basePrice={selectedUnit?.base_price}
          />

          <ProposalForm
            title="Fluxo da proposta"
            rows={state.saleFlowRows}
            onRowChange={(index, field, value) => state.updateSaleRow(index, field, value, selectedUnit?.base_price)}
            onAddRow={state.addSaleRow}
            onRemoveRow={state.removeSaleRow}
            basePrice={selectedUnit?.base_price}
          />

          {isPermuta ? (
            <ProposalForm
              title="Fluxo de permuta"
              rows={state.exchangeFlowRows}
              onRowChange={(index, field, value) => state.updateExchangeRow(index, field, value, selectedUnit?.base_price)}
              basePrice={selectedUnit?.base_price}
            />
          ) : null}
        </div>
      </section>

      <aside className="flex flex-col gap-6 xl:col-span-4">
        <Card>
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-city-blue-dark">Resumo e simulação</h2>
            <div className="mt-3 flex w-full items-center gap-1 rounded-full border border-[#e5d7c3] bg-[#fff8ef] p-1">
              <button
                className={`flex-1 cursor-pointer whitespace-nowrap rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                  !isPermuta
                    ? 'bg-city-blue text-city-blue-dark shadow-sm'
                    : 'text-text-muted hover:text-text-main'
                }`}
                onClick={() => state.setScenarioMode('NORMAL')}
              >
                Venda Normal
              </button>
              <button
                className={`flex flex-1 cursor-pointer items-center justify-center gap-2 whitespace-nowrap rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                  isPermuta
                    ? 'bg-city-blue text-city-blue-dark shadow-sm'
                    : 'text-text-muted hover:text-text-main'
                }`}
                onClick={() => state.setScenarioMode('PERMUTA')}
              >
                <ArrowRightLeft className="h-4 w-4" />
                Com Permuta
              </button>
            </div>
          </div>
          <Button
            className="w-full py-3 text-base"
            variant="primary"
            onClick={handleCalculate}
            disabled={!canCalculate || calculating}
          >
            <Calculator className="mr-2 h-5 w-5" />
            {calculating ? 'Calculando...' : 'Calcular cenário'}
          </Button>

          <SummaryCard summary={summary} warnings={result?.warnings} isPermuta={isPermuta} />
        </Card>

        <EconomicIndicators
          result={result}
          productContext={state.productContext}
          selectedUnit={selectedUnit}
          isPermuta={isPermuta}
        />
      </aside>
    </main>
  );
}
