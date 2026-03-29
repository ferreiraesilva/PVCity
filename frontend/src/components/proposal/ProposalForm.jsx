import React from 'react';
import { Card } from '../shared/Card';
import { Input } from '../shared/Input';
import { Select } from '../shared/Select';

const PERIODICITY_OPTIONS = [
  'Sinal',
  'Entrada',
  'Mensais',
  'Semestrais',
  'Única',
  'Permuta',
  'Anuais',
  'Veículo',
  'Financ. Bancário',
  'Financ. Direto',
];

const ADJUSTMENT_OPTIONS = [
  'Fixas Irreajustaveis',
  'INCC',
  'IGPM + 12% a.a',
  'IPCA + 0,99% a.m',
  'IPCA + 13,65% a.a',
];

const BRL = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });

function toLocalePercent(val) {
  if (val === null || val === undefined || val === '') return '';
  return (Number(val) * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fromLocaleValue(val) {
  if (typeof val !== 'string') return val;
  const cleaned = val.replace(/\./g, '').replace(',', '.').replace(/[^\d.-]/g, '');
  const num = parseFloat(cleaned);
  return isNaN(num) ? '' : num;
}

function formatDisplayValue(val) {
  if (val === null || val === undefined || val === '') return '';
  return Number(val).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function ProposalForm({
  rows,
  onRowChange,
  title = 'Cronograma de Pagamento',
  readOnly = false,
}) {
  const cols = 'grid-cols-[4fr_10fr_8fr_10fr_6fr_10fr_11fr]';

  return (
    <Card className="overflow-x-auto">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <div className="city-kicker mb-1 text-[#b27619]">{readOnly ? 'Referência' : 'Proposta'}</div>
          <h2 className="text-lg font-semibold text-city-blue-dark">{title}</h2>
        </div>
        {readOnly ? (
          <span className="rounded-full border border-[#e8d8bf] bg-[#fff4e4] px-3 py-1 text-xs font-medium text-[#8f6321]">
            Visualização padrão
          </span>
        ) : null}
      </div>

      <div className="min-w-[860px]">
        <div className={`mb-3 grid ${cols} gap-3 border-b border-border-color pb-3 text-[10px] font-black uppercase tracking-widest text-[#4a4855]/40`}>
          <div>Parcelas</div>
          <div>Periodicidade</div>
          <div>Mês Início</div>
          <div className="text-right">Valor Unitário</div>
          <div className="text-right">% VGV</div>
          <div className="text-right font-bold text-city-blue-dark">Total (PV)</div>
          <div>Reajuste</div>
        </div>

        <div className="flex flex-col gap-2">
          {rows.map((row, index) => {
            if (readOnly && !row.installment_count && !row.installment_value && !row.total_vgv) {
              return null;
            }

            if (readOnly) {
              return (
                <div
                  key={row.row_slot ?? index}
                  className={`grid ${cols} items-center gap-3 rounded-[20px] border border-[#efe4d7] bg-[#fffaf3] px-4 py-3 text-sm text-text-main`}
                >
                  <div className="font-mono font-bold text-[#b27619]">{row.installment_count || '–'}</div>
                  <div className="font-semibold">{row.periodicity || '–'}</div>
                  <div className="text-text-muted">{row.start_month || '–'}</div>
                  <div className="text-right font-medium">
                    {row.installment_value != null && row.installment_value !== ''
                      ? BRL.format(row.installment_value)
                      : '–'}
                  </div>
                  <div className="text-right text-text-muted">
                    {row.percent != null && row.percent !== ''
                      ? `${(Number(row.percent) * 100).toFixed(2)}%`
                      : '–'}
                  </div>
                  <div className="text-right font-bold text-city-blue-dark">
                    {row.total_vgv != null && row.total_vgv !== '' ? BRL.format(row.total_vgv) : '–'}
                  </div>
                  <div className="text-xs font-medium uppercase text-slate-400">{row.adjustment_type || '–'}</div>
                </div>
              );
            }

            return (
              <div key={row.row_slot ?? index} className={`group grid ${cols} items-center gap-3`}>
                <Input
                  type="number"
                  value={row.installment_count}
                  onChange={(event) =>
                    onRowChange(index, 'installment_count', event.target.value ? Number(event.target.value) : '')
                  }
                  inputClassName="text-center font-bold"
                  className="h-11"
                />

                <Select
                  options={PERIODICITY_OPTIONS}
                  value={row.periodicity || ''}
                  onChange={(event) => onRowChange(index, 'periodicity', event.target.value)}
                  className="h-11"
                />

                <Input
                  type="date"
                  value={row.start_month}
                  onChange={(event) => onRowChange(index, 'start_month', event.target.value)}
                  className="h-11"
                  inputClassName="text-xs"
                />

                <Input
                  prefix="R$"
                  value={formatDisplayValue(row.installment_value)}
                  onChange={(event) => {
                    // Allow only digits and one comma for typing
                    const raw = event.target.value;
                    onRowChange(index, 'installment_value', fromLocaleValue(raw));
                  }}
                  inputClassName="text-right font-medium"
                  className="h-11"
                />

                <Input
                  suffix="%"
                  value={toLocalePercent(row.percent)}
                  onChange={(event) => {
                    const val = fromLocaleValue(event.target.value);
                    onRowChange(index, 'percent', val !== '' ? val / 100 : '');
                  }}
                  inputClassName="text-right font-medium"
                  className="h-11"
                />

                <Input
                  prefix="R$"
                  value={formatDisplayValue(row.total_vgv || (row.installment_count * row.installment_value))}
                  onChange={(event) => {
                    onRowChange(index, 'total_vgv', fromLocaleValue(event.target.value));
                  }}
                  inputClassName="text-right font-bold text-city-blue-dark"
                  className="h-11"
                  disabled
                />

                <Select
                  options={ADJUSTMENT_OPTIONS}
                  value={row.adjustment_type || ''}
                  onChange={(event) => onRowChange(index, 'adjustment_type', event.target.value)}
                  className="h-11"
                  containerClassName="text-xs"
                />
              </div>
            );
          })}
        </div>
      </div>
    </Card>
  );
}
