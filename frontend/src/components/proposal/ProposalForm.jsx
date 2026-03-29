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

export function ProposalForm({
  rows,
  onRowChange,
  title = 'Cronograma de Pagamento',
  readOnly = false,
}) {
  const cols = 'grid-cols-[5rem_10rem_8rem_9rem_5rem_9rem_11rem]';

  return (
    <Card className="overflow-x-auto">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <div className="city-kicker mb-1 text-[#b27619]">{readOnly ? 'Referência' : 'Proposta'}</div>
          <h2 className="text-lg font-semibold text-city-blue-dark">{title}</h2>
        </div>
        {readOnly ? (
          <span className="rounded-full border border-[#e8d8bf] bg-[#fff4e4] px-3 py-1 text-xs font-medium text-[#8f6321]">
            Somente leitura
          </span>
        ) : null}
      </div>

      <div className="min-w-[760px]">
        <div className={`mb-2 grid ${cols} gap-2 border-b border-border-color pb-2 text-xs font-medium uppercase tracking-wider text-text-muted`}>
          <div>Parcelas</div>
          <div>Periodicidade</div>
          <div>Mês Início</div>
          <div>Valor (R$)</div>
          <div>% VGV</div>
          <div>Total (R$)</div>
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
                  className={`grid ${cols} items-center gap-2 rounded-[18px] border border-[#efe4d7] bg-[#fffaf3] px-3 py-2 text-sm text-text-main`}
                >
                  <div className="font-mono">{row.installment_count || '–'}</div>
                  <div>{row.periodicity || '–'}</div>
                  <div>{row.start_month || '–'}</div>
                  <div className="font-medium">
                    {row.installment_value != null && row.installment_value !== ''
                      ? BRL.format(row.installment_value)
                      : '–'}
                  </div>
                  <div>
                    {row.percent != null && row.percent !== ''
                      ? `${(Number(row.percent) * 100).toFixed(2)}%`
                      : '–'}
                  </div>
                  <div className="font-medium">
                    {row.total_vgv != null && row.total_vgv !== '' ? BRL.format(row.total_vgv) : '–'}
                  </div>
                  <div className="text-xs text-text-muted">{row.adjustment_type || '–'}</div>
                </div>
              );
            }

            return (
              <div key={row.row_slot ?? index} className={`grid ${cols} items-center gap-2`}>
                <Input
                  type="number"
                  value={row.installment_count}
                  onChange={(event) =>
                    onRowChange(index, 'installment_count', event.target.value ? Number(event.target.value) : '')
                  }
                  className="h-11 px-3 py-2 text-sm"
                />

                <Select
                  options={PERIODICITY_OPTIONS}
                  value={row.periodicity || ''}
                  onChange={(event) => onRowChange(index, 'periodicity', event.target.value)}
                  className="h-11 px-3 py-2 text-sm"
                />

                <Input
                  type="date"
                  value={row.start_month}
                  onChange={(event) => onRowChange(index, 'start_month', event.target.value)}
                  className="h-11 px-3 py-2 text-sm"
                />

                <Input
                  type="number"
                  step="0.01"
                  value={row.installment_value}
                  onChange={(event) =>
                    onRowChange(index, 'installment_value', event.target.value ? Number(event.target.value) : '')
                  }
                  className="h-11 px-3 py-2 text-sm"
                />

                <Input
                  type="number"
                  step="0.0001"
                  value={row.percent}
                  onChange={(event) => onRowChange(index, 'percent', event.target.value ? Number(event.target.value) : '')}
                  className="h-11 px-3 py-2 text-sm"
                />

                <Input
                  type="number"
                  step="0.01"
                  value={row.total_vgv}
                  onChange={(event) =>
                    onRowChange(index, 'total_vgv', event.target.value ? Number(event.target.value) : '')
                  }
                  className="h-11 bg-[#fbf6ef] px-3 py-2 text-sm"
                />

                <Select
                  options={ADJUSTMENT_OPTIONS}
                  value={row.adjustment_type || ''}
                  onChange={(event) => onRowChange(index, 'adjustment_type', event.target.value)}
                  className="h-11 px-3 py-2 text-sm"
                />
              </div>
            );
          })}
        </div>
      </div>
    </Card>
  );
}
