import React, { useMemo } from 'react';
import { 
  TrendingUp, 
  Calendar, 
  DollarSign, 
  Percent,
  ArrowUpRight,
  ArrowDownRight,
  TrendingDown,
  Target,
  Info
} from 'lucide-react';
import { Card } from '../shared/Card';
import { clsx } from 'clsx';

const BRL = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });

function formatBRL(value) {
  return value != null ? BRL.format(value) : '--';
}

function formatPct(value) {
  if (value == null) return '--';
  return `${(value * 100).toFixed(2)}%`;
}

function MetricCard({ title, icon: Icon, children, className, tooltip }) {
  return (
    <div className={clsx("rounded-[24px] border border-border-color bg-[#fffdf9] p-5 shadow-sm transition-all hover:shadow-md", className)}>
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2 text-text-muted">
          <Icon className="h-4 w-4" />
          <span className="text-[0.7rem] font-bold uppercase tracking-widest">{title}</span>
        </div>

        {tooltip && (
          <div className="group relative">
            <Info className="h-4 w-4 cursor-help text-text-muted hover:text-text-main" />
            <div className="invisible absolute right-0 top-6 z-10 w-64 rounded-[18px] border border-border-color bg-[#fffdf9] p-3 shadow-xl opacity-0 transition-opacity group-hover:visible group-hover:opacity-100">
              <div className="mb-1 text-[0.65rem] font-bold uppercase text-text-muted">Entenda a Métrica</div>
              <p className="text-xs leading-relaxed text-text-main font-normal normal-case tracking-normal">
                {tooltip}
              </p>
            </div>
          </div>
        )}
      </div>
      {children}
    </div>
  );
}

export function EconomicIndicators({ result, productContext, selectedUnit, isPermuta }) {
  const summary = isPermuta ? result?.summary?.permuta : result?.summary?.normal;
  const flow = isPermuta ? result?.exchange_monthly_flow : result?.sale_monthly_flow;

  if (!summary || !selectedUnit) return null;

  const area = selectedUnit.private_area_m2 || 1;
  const standardM2 = (summary.standard_total_pv || summary.table_total_vgv) / area;
  const proposalM2 = (isPermuta ? summary.exchange_total_pv : summary.proposal_total_pv) / area;
  const m2Variation = ((proposalM2 / standardM2) - 1);
  const deliveryMonthStr = productContext.delivery_month;

  const metrics = useMemo(() => {
    if (!flow || !deliveryMonthStr) return null;
    let weightedOffsetSum = 0;
    let totalGrossPreDelivery = 0;
    flow.forEach(event => {
      if (event.month <= deliveryMonthStr) {
        const gross = (event.gross_adjustable || 0) + (event.gross_fixed || 0);
        weightedOffsetSum += gross * event.month_offset;
        totalGrossPreDelivery += gross;
      }
    });

    const averageOffset = totalGrossPreDelivery > 0 ? weightedOffsetSum / totalGrossPreDelivery : 0;
    const preDeliveryPercent = totalGrossPreDelivery / (isPermuta ? summary.exchange_total_vgv : summary.proposal_total_vgv);

    return { averageOffset, preDeliveryPercent, totalGrossPreDelivery };
  }, [flow, deliveryMonthStr, summary, isPermuta]);

  const pvDifference = proposalM2 * area - standardM2 * area;
  const efficiency = proposalM2 * area / (isPermuta ? summary.exchange_total_vgv : summary.proposal_total_vgv);

  return (
    <Card className="mt-6">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-city-blue-dark">
          Métricas de Performance
        </h2>
      </div>

      <div className="flex flex-col gap-5">
        {/* 1. VALOR DO M2 - FOCO TOTAL EM LEITURA */}
        <MetricCard 
          title="Valor do M² (VPL)" 
          icon={TrendingUp}
          tooltip="Valor presente por metro quadrado. Permite comparar o valor real da proposta com a tabela, descontando o custo do tempo e inflação implícita."
        >
          <div className="flex flex-col gap-1">
            <div className="flex items-baseline justify-between">
              <span className="text-4xl font-black tracking-tighter text-city-blue-dark">
                {formatBRL(proposalM2)}
              </span>
              <div className={clsx(
                "flex items-center gap-1 rounded-full px-3 py-1 text-xs font-black",
                m2Variation >= 0 ? "bg-success-green/10 text-success-green" : "bg-danger-red/10 text-danger-red"
              )}>
                {m2Variation >= 0 ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
                {formatPct(Math.abs(m2Variation))}
              </div>
            </div>
            <div className="mt-2 flex items-center gap-2 border-t border-border-color/40 pt-2 text-xs text-text-muted">
              <div className="font-medium uppercase tracking-tight">Referência de Tabela:</div>
              <div className="font-bold text-text-main line-through decoration-danger-red/30 opacity-60">
                {formatBRL(standardM2)}
              </div>
            </div>
          </div>
        </MetricCard>

        {/* 2. RECEBIMENTO E CAPTURA */}
        <MetricCard 
          title="Recebimento (Pré-Chaves)" 
          icon={Calendar}
          tooltip="Métricas de prazo e volume financeiro que o incorporador coloca no caixa antes de entregar as chaves da unidade."
        >
          <div className="flex flex-col gap-4">
            <div className="flex items-end justify-between">
              <div>
                <div className="text-[0.6rem] font-bold uppercase text-slate-400">Tempo Médio</div>
                <div className="text-3xl font-black text-slate-800">
                  {metrics ? metrics.averageOffset.toFixed(1) : '--'} 
                  <span className="ml-1 text-sm font-medium text-slate-400">meses</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-[0.6rem] font-bold uppercase text-slate-400">Valor Médio</div>
                <div className="text-2xl font-black text-city-blue">
                   {metrics ? formatBRL(metrics.totalGrossPreDelivery / (metrics.averageOffset || 1)) : '--'}
                </div>
              </div>
            </div>

            {/* BARRA DE PROGRESSO PREMIUM */}
            <div className="space-y-1.5">
              <div className="relative h-2 w-full overflow-hidden rounded-full bg-slate-100">
                <div 
                  className="h-full bg-gradient-to-r from-city-blue to-city-blue-dark shadow-[0_0_10px_rgba(40,154,255,0.4)] transition-all duration-1000"
                  style={{ width: metrics ? `${Math.min(metrics.preDeliveryPercent * 100, 100)}%` : '0%' }}
                />
              </div>
              <div className="flex justify-between text-[10px] font-bold uppercase text-slate-400">
                <span>Data-Base</span>
                <span>{deliveryMonthStr || 'Chaves'}</span>
              </div>
            </div>
          </div>
        </MetricCard>

        {/* 3. MINI CARDS RESUMOS */}
        <div className="grid grid-cols-2 gap-3">
          <div className="relative rounded-[22px] bg-white p-4 shadow-sm border border-slate-100">
            <div className="mb-1 flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-[0.6rem] font-black uppercase text-slate-400">
                <Percent className="h-3 w-3" />
                Eficiência
              </div>
              <div className="group relative">
                <Info className="h-3 w-3 cursor-help text-slate-300 hover:text-slate-500" />
                <div className="invisible absolute right-0 top-5 z-10 w-48 rounded-[14px] border border-border-color bg-white p-3 shadow-lg opacity-0 transition-opacity group-hover:visible group-hover:opacity-100">
                  <p className="text-[10px] leading-relaxed text-text-main font-normal normal-case tracking-normal">
                    Razão entre Valor Presente e Valor Nominal. Indica quanto do valor total é preservado financeiramente.
                  </p>
                </div>
              </div>
            </div>
            <div className="text-lg font-black text-slate-800">{formatPct(efficiency)}</div>
          </div>

          <div className="relative rounded-[22px] bg-white p-4 shadow-sm border border-slate-100">
            <div className="mb-1 flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-[0.6rem] font-black uppercase text-slate-400">
                <Target className="h-3 w-3" />
                Impacto
              </div>
              <div className="group relative">
                <Info className="h-3 w-3 cursor-help text-slate-300 hover:text-slate-500" />
                <div className="invisible absolute right-0 top-5 z-10 w-48 rounded-[14px] border border-border-color bg-white p-3 shadow-lg opacity-0 transition-opacity group-hover:visible group-hover:opacity-100">
                  <p className="text-[10px] leading-relaxed text-text-main font-normal normal-case tracking-normal">
                    Diferença absoluta em Reais entre o VPL da proposta e o padrão.
                  </p>
                </div>
              </div>
            </div>
            <div className={clsx(
              "text-lg font-black",
              pvDifference >= 0 ? "text-success-green" : "text-danger-red"
            )}>
              {formatBRL(pvDifference)}
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}
