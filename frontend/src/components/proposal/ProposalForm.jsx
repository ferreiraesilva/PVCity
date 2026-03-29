import { Plus, Trash2, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { Card } from '../shared/Card';
import { CurrencyInput } from '../shared/CurrencyInput';
import { Input } from '../shared/Input';
import { Select } from '../shared/Select';
import { Button } from '../shared/Button';

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

// Utility functions for read-only table display
function toLocalePercentDisplay(val) {
  if (val === null || val === undefined || val === '') return '–';
  return `${(Number(val) * 100).toFixed(2)}%`;
}

export function ProposalForm({
  rows,
  onRowChange,
  onAddRow,
  onRemoveRow,
  title = 'Cronograma de Pagamento',
  readOnly = false,
  basePrice = 0,
}) {
  const cols = readOnly 
    ? 'grid-cols-[4fr_11fr_9fr_13fr_5fr_13fr_11fr]'
    : 'grid-cols-[4fr_11fr_9fr_13fr_5fr_13fr_11fr_50px]';

  const totalProposal = rows.reduce((acc, row) => acc + (Number(row.total_vgv) || 0), 0);
  const diff = totalProposal - basePrice;
  const isDivergent = Math.abs(diff) > 0.01; // Avoid floating point noise

  return (
    <Card className="overflow-x-auto border-none !p-0 shadow-sm bg-white/40 ring-1 ring-slate-200/50">
      <div className="flex items-center justify-between border-b border-slate-100 bg-slate-50/30 px-6 py-4">
        <div>
          <div className="city-kicker mb-0.5 text-[10px] text-[#b27619] uppercase font-black">{readOnly ? 'Referência' : 'Proposta'}</div>
          <h2 className="text-base font-bold text-city-blue-dark">{title}</h2>
        </div>
        {readOnly ? (
          <span className="rounded-full border border-blue-100 bg-blue-50 px-2.5 py-1 text-[10px] font-black uppercase text-blue-600 tracking-tight">
            Tabela de Referência
          </span>
        ) : null}
      </div>

      <div className="min-w-[900px]">
        <div className={`grid ${cols} gap-1 border-b border-slate-100 bg-slate-50/50 px-4 py-2.5 text-[10px] font-black uppercase tracking-wider text-slate-400`}>
          <div className="pl-2">Qtd</div>
          <div>Periodicidade</div>
          <div>Mês Início</div>
          <div className="text-right">Valor Unitário</div>
          <div className="text-right">% VGV</div>
          <div className="text-right font-bold text-city-blue-dark">Total da Série</div>
          <div className="pl-4">Reajuste</div>
          {!readOnly && <div className="text-center"></div>}
        </div>

        <div className="flex flex-col">
          {rows.map((row, index) => {
            const hasData = row.installment_count || row.installment_value || row.total_vgv;
            
            if (readOnly && !hasData) return null;

            if (readOnly) {
                return (
                  <div
                    key={row.row_slot ?? index}
                    className={`grid ${cols} items-center gap-1 border-b border-slate-50 px-4 py-2 text-xs transition-colors hover:bg-slate-50/30`}
                  >
                    <div className="pl-2 font-mono font-bold text-slate-600">{row.installment_count || '–'}</div>
                    <div className="font-semibold text-slate-700">{row.periodicity || '–'}</div>
                    <div className="text-slate-400 font-medium">{row.start_month || '–'}</div>
                    <div className="text-right font-bold text-slate-700">
                      {row.installment_value != null && row.installment_value !== ''
                        ? BRL.format(row.installment_value)
                        : '–'}
                    </div>
                    <div className="text-right font-medium text-slate-400">
                      {toLocalePercentDisplay(row.percent)}
                    </div>
                    <div className="text-right font-black text-city-blue-dark">
                      {row.total_vgv != null && row.total_vgv !== '' ? BRL.format(row.total_vgv) : '–'}
                    </div>
                    <div className="pl-4 text-[10px] font-black uppercase text-slate-300">{row.adjustment_type || '–'}</div>
                  </div>
                );
              }

              return (
                <div key={row.row_slot ?? index} className={`grid ${cols} items-center gap-1 border-b border-slate-50 px-4 py-1.5 transition-colors hover:bg-slate-50/50 group`}>
                  <div className="pl-2">
                    <Input
                      type="number"
                      variant="minimal"
                      size="sm"
                      value={row.installment_count}
                      onChange={(event) =>
                        onRowChange(index, 'installment_count', event.target.value ? Number(event.target.value) : '')
                      }
                      inputClassName="font-bold text-city-blue-dark text-center !py-1"
                    />
                  </div>

                  <div>
                    <Select
                      variant="minimal"
                      size="sm"
                      options={PERIODICITY_OPTIONS}
                      value={row.periodicity || ''}
                      onChange={(event) => onRowChange(index, 'periodicity', event.target.value)}
                      className="!py-0"
                    />
                  </div>

                  <div>
                    <Input
                      type="date"
                      variant="minimal"
                      size="sm"
                      value={row.start_month}
                      onChange={(event) => onRowChange(index, 'start_month', event.target.value)}
                      inputClassName="text-slate-500 !py-1"
                    />
                  </div>

                  <div>
                    <CurrencyInput
                      prefix="R$"
                      value={row.installment_value}
                      onValueChange={(val) => onRowChange(index, 'installment_value', val)}
                      inputClassName="text-right font-bold text-slate-700 !py-1"
                    />
                  </div>

                  <div>
                    <CurrencyInput
                      suffix="%"
                      value={row.percent ? row.percent * 100 : ''}
                      onValueChange={(val) => onRowChange(index, 'percent', val !== '' ? val / 100 : '')}
                      inputClassName="text-right font-medium text-slate-400 !py-1"
                    />
                  </div>

                  <div>
                    <CurrencyInput
                      prefix="R$"
                      value={row.total_vgv || (row.installment_count * row.installment_value)}
                      disabled
                      inputClassName="text-right font-black text-city-blue-dark !py-1"
                    />
                  </div>

                  <div className="pl-4">
                    <Select
                      variant="minimal"
                      size="sm"
                      options={ADJUSTMENT_OPTIONS}
                      value={row.adjustment_type || ''}
                      onChange={(event) => onRowChange(index, 'adjustment_type', event.target.value)}
                      className="!py-0"
                      containerClassName="text-[10px] font-black uppercase text-slate-400"
                    />
                  </div>
                  <div className="text-center">
                    <button
                      onClick={() => onRemoveRow(index)}
                      className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-300 transition-all hover:bg-danger-red/10 hover:text-danger-red opacity-0 group-hover:opacity-100"
                      title="Remover Série"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
              );
            })}

          {/* Totals Summary Row */}
          <div className={`grid ${cols} items-center gap-1 bg-slate-50/20 px-4 py-3 border-t border-slate-100`}>
            <div className="col-span-3 flex items-center gap-3">
              <span className="text-[10px] font-black uppercase text-slate-400 tracking-wider">Total do Fluxo</span>
              {isDivergent && (
                <div className={`flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[10px] font-black uppercase tracking-tight ${
                  diff < 0 
                    ? 'bg-amber-50 text-amber-600 border border-amber-100' 
                    : 'bg-emerald-50 text-emerald-600 border border-emerald-100'
                }`}>
                  <AlertTriangle size={12} />
                  <span>{diff < 0 ? 'Desconto:' : 'Ágio:'} {BRL.format(Math.abs(diff))}</span>
                </div>
              )}
              {!isDivergent && basePrice > 0 && (
                <div className="flex items-center gap-1.5 rounded-full bg-slate-50 border border-slate-100 px-2.5 py-1 text-[10px] font-black uppercase tracking-tight text-slate-400">
                  <CheckCircle2 size={12} />
                  <span>Valor em Paridade</span>
                </div>
              )}
            </div>
            <div className="col-span-2"></div>
            <div className="text-right font-black text-city-blue-dark text-sm pr-1">
              {BRL.format(totalProposal)}
            </div>
            <div className="pl-4">
              <div className="text-[10px] font-black uppercase text-slate-300">Total Proposta</div>
            </div>
            {!readOnly && <div></div>}
          </div>
        </div>
      </div>

      {!readOnly && (
        <div className="border-t border-slate-50 bg-white/50 p-4">
          <Button
            variant="outline"
            size="sm"
            onClick={onAddRow}
            className="w-full border-dashed border-slate-200 text-slate-400 hover:border-city-blue hover:text-city-blue"
          >
            <Plus size={14} className="mr-2" />
            Adicionar Série de Pagamento
          </Button>
        </div>
      )}
    </Card>
  );
}
