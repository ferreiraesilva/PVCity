import React, { useState } from 'react';
import { Card } from '../shared/Card';
import { Input } from '../shared/Input';
import { Button } from '../shared/Button';
import { Percent, TrendingUp, Info, Save, CheckCircle2 } from 'lucide-react';
import { services } from '../../api/services';

export function FinancialParamsWorkspace({ financialRates, onUpdateRates }) {
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Conversão de anual para mensal para exibição amigável
  // i_mensal = (1 + i_anual)^(1/12) - 1
  const monthlyRate = Math.pow(1 + (financialRates.vpl_rate_annual || 0), 1 / 12) - 1;

  const handleMonthlyChange = (e) => {
    const mValue = parseFloat(e.target.value) / 100;
    if (isNaN(mValue)) return;
    
    // Converte de volta para anual para o estado
    // i_anual = (1 + i_mensal)^12 - 1
    const aValue = Math.pow(1 + mValue, 12) - 1;
    onUpdateRates('vpl_rate_annual', aValue);
    setSaveSuccess(false);
  };

  const handleAnnualChange = (e) => {
    const aValue = parseFloat(e.target.value) / 100;
    if (isNaN(aValue)) return;
    onUpdateRates('vpl_rate_annual', aValue);
    setSaveSuccess(false);
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      await services.updateConfig('vpl_rate_annual', financialRates.vpl_rate_annual);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (error) {
      alert('Falha ao salvar parâmetro no banco de dados.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="animate-in fade-in duration-500 space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-8 border-[#e5d7c3]/30 bg-white shadow-sm overflow-hidden relative">
          <div className="absolute top-0 right-0 p-4 opacity-5">
            <Percent size={120} />
          </div>
          
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-city-blue/10 text-city-blue">
                <TrendingUp size={20} />
              </div>
              <h3 className="text-lg font-bold text-text-main">Taxa de Desconto (VPL)</h3>
            </div>
            
            <Button 
              variant={saveSuccess ? "outline" : "primary"}
              size="sm"
              onClick={handleSave}
              disabled={isSaving}
              className={saveSuccess ? "border-green-500 text-green-600" : ""}
            >
              {isSaving ? (
                'Salvando...'
              ) : saveSuccess ? (
                <><CheckCircle2 size={16} className="mr-2" /> Salvo</>
              ) : (
                <><Save size={16} className="mr-2" /> Salvar taxa</>
              )}
            </Button>
          </div>

          <div className="space-y-6 relative z-10">
            <div>
              <label className="block text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">
                Taxa mensal para simulação
              </label>
              <div className="flex items-center gap-3">
                <div className="flex-1">
                  <Input
                    type="number"
                    step="0.0001"
                    value={(monthlyRate * 100).toFixed(4)}
                    onChange={handleMonthlyChange}
                    className="text-2xl font-bold h-14"
                  />
                </div>
                <div className="text-xl font-bold text-text-muted">% a.m.</div>
              </div>
            </div>

            <div className="pt-4 border-t border-dashed border-border-color">
              <label className="block text-xs font-semibold text-text-muted mb-2 uppercase tracking-wider">
                Equivalente anual (taxa nominal no sistema)
              </label>
              <div className="flex items-center gap-3">
                <div className="flex-1">
                  <Input
                    type="number"
                    step="0.0001"
                    value={(financialRates.vpl_rate_annual * 100).toFixed(4)}
                    onChange={handleAnnualChange}
                    className="text-lg font-medium text-text-muted bg-gray-50/50"
                  />
                </div>
                <div className="text-sm font-semibold text-text-muted">% a.a.</div>
              </div>
            </div>
          </div>
          
          <div className="mt-8 p-4 rounded-2xl bg-amber-50 border border-amber-100 flex gap-3">
            <Info size={18} className="text-amber-600 shrink-0 mt-0.5" />
            <p className="text-xs text-amber-800 leading-relaxed">
              Esta taxa é utilizada como <strong>Taxa Mínima de Atratividade (TMA)</strong> para descontar todos os fluxos de caixa futuros. 
              Alterá-la mudará o PV de referência e da proposta imediatamente.
            </p>
          </div>
        </Card>

        <Card className="p-8 border-[#e5d7c3]/30 bg-gray-50/30 flex items-center justify-center border-dashed">
          <div className="text-center space-y-3 opacity-40">
            <div className="mx-auto w-12 h-12 rounded-full border-2 border-dashed border-gray-400 flex items-center justify-center">
               <span className="text-xl">...</span>
            </div>
            <p className="text-sm font-medium italic">Novos parâmetros em breve</p>
          </div>
        </Card>
      </div>
    </div>
  );
}
