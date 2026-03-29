import React from 'react';
import { clsx } from 'clsx';
import {
  AlertTriangle,
  BadgeDollarSign,
  Info,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
} from 'lucide-react';

const BRL = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });

function formatBRL(value) {
  return value != null ? BRL.format(value) : '--';
}

function formatPct(value, signed = false) {
  if (value == null) return '--';
  const pct = (value * 100).toFixed(2);
  return signed && value > 0 ? `+${pct}%` : `${pct}%`;
}

export function SummaryCard({ summary, warnings, isPermuta }) {
  if (!summary) {
    return (
      <div className="mt-4 rounded-[22px] border border-border-color bg-[#fffaf3] p-4 text-sm text-text-muted">
        Nenhum cenário calculado. Selecione a unidade, revise o fluxo e calcule.
      </div>
    );
  }

  const {
    pv_status,
    risk_level,
    risk_reasons,
    commission_status,
    capture_total_percent,
    commission_total_percent,
    commission_total_value,
    pv_variation_percent,
    exchange_vpl_variation_percent,
    table_total_vgv,
    proposal_total_pv,
    standard_total_pv,
  } = summary;

  const variationPercent = exchange_vpl_variation_percent ?? pv_variation_percent ?? null;
  const isApproved = pv_status?.includes('Aprovado');
  const isHighRisk = risk_level?.toLowerCase() === 'alto';
  const variationPositive = variationPercent != null && variationPercent > 0;

  return (
    <div className="mt-4 flex flex-col gap-4">
      <div
        className={clsx(
          'flex items-center justify-between rounded-[24px] border p-4',
          isApproved
            ? 'border-success-green/30 bg-[#eef8f2] text-success-green'
            : 'border-danger-red/40 bg-[#fff2f1] text-danger-red'
        )}
      >
        <div className="flex items-center gap-3">
          {isApproved ? <ShieldCheck className="h-8 w-8" /> : <ShieldAlert className="h-8 w-8" />}
          <div>
            <h3 className="text-lg font-semibold">{pv_status || 'Pendente'}</h3>
            <div className="text-sm opacity-80">
              {isPermuta ? 'Status do trilho com permuta' : 'Status da proposta'}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div className="rounded-[22px] border border-border-color bg-[#fffdf9] p-4">
          <div className="mb-1 flex items-center gap-2 text-text-muted">
            <TrendingUp className="h-4 w-4" />
            <span className="text-sm font-medium">Captura Total</span>
          </div>
          <div className="text-2xl font-bold text-text-main">{formatPct(capture_total_percent)}</div>
        </div>

        <div
          className={clsx(
            'relative rounded-[22px] border p-4',
            isHighRisk ? 'border-danger-red/30 bg-[#fff2f1]' : 'border-border-color bg-[#fffdf9]'
          )}
        >
          <div className="mb-1 flex items-center justify-between text-text-muted">
            <div className="flex items-center gap-2">
              <AlertTriangle className={clsx('h-4 w-4', isHighRisk && 'text-danger-red')} />
              <span className="text-sm font-medium">Nível de Risco</span>
            </div>

            <div className="group relative">
              <Info className="h-4 w-4 cursor-help text-text-muted hover:text-text-main" />
              <div className="invisible absolute right-0 top-6 z-10 w-64 rounded-[18px] border border-border-color bg-[#fffdf9] p-3 shadow-xl opacity-0 transition-opacity group-hover:visible group-hover:opacity-100">
                <div className="mb-1 text-xs font-bold uppercase text-text-muted">Análise de Risco</div>
                <ul className="space-y-1.5">
                  {risk_reasons?.map((reason, index) => (
                    <li key={index} className="flex gap-2 text-xs text-text-main">
                      <span className="text-city-blue">•</span>
                      {reason}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          <div className={clsx('text-2xl font-bold', isHighRisk ? 'text-danger-red' : 'text-text-main')}>
            {risk_level || '--'}
          </div>
        </div>
      </div>

      <div className="rounded-[22px] border border-border-color bg-[#fffdf9] p-4">
        <div className="mb-3 text-sm font-semibold text-text-main">Análise de PV (VPL)</div>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <div className="text-text-muted">PV Padrão</div>
            <div className="font-bold text-text-main">{formatBRL(standard_total_pv || table_total_vgv)}</div>
          </div>
          <div>
            <div className="text-text-muted">PV da Proposta</div>
            <div className="font-bold text-text-main">{formatBRL(proposal_total_pv)}</div>
          </div>
        </div>
        <div className="mt-3 flex items-center justify-between border-t border-border-color pt-3">
          <span className="text-sm text-text-muted">Variação de Eficiência</span>
          <span
            className={clsx(
              'text-lg font-bold',
              variationPercent == null
                ? 'text-text-muted'
                : variationPositive
                  ? 'text-success-green'
                  : variationPercent < 0
                    ? 'text-danger-red'
                    : 'text-text-main'
            )}
          >
            {formatPct(variationPercent, true)}
          </span>
        </div>
      </div>

      <div className="rounded-[22px] border border-[#f1d4aa] bg-[#fff4e4] p-4">
        <div className="mb-2 flex items-center gap-2 text-city-blue-dark">
          <BadgeDollarSign className="h-5 w-5" />
          <h3 className="font-semibold">Comissionamento ({commission_status || '--'})</h3>
        </div>
        <div className="flex justify-between gap-4">
          <div>
            <div className="text-sm text-text-muted">Percentual Total</div>
            <div className="text-xl font-bold text-text-main">{formatPct(commission_total_percent)}</div>
          </div>
          <div className="text-right">
            <div className="text-sm text-text-muted">Valor Total</div>
            <div className="text-xl font-bold text-text-main">{formatBRL(commission_total_value)}</div>
          </div>
        </div>
      </div>

      {warnings && warnings.length > 0 ? (
        <div className="rounded-[22px] border border-warning-yellow/50 bg-[#fff4de] p-4">
          <h4 className="mb-2 flex items-center gap-2 text-sm font-semibold text-[#a46a10]">
            <AlertTriangle className="h-4 w-4" />
            Alertas de paridade
          </h4>
          <ul className="space-y-1 pl-5 text-sm text-[#8f6a2f]">
            {warnings.map((warning) => (
              <li key={warning.code} className="list-disc">
                {warning.message}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
