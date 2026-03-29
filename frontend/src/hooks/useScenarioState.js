import { useState } from 'react';

const EMPTY_ROWS = Array.from({ length: 20 }, (_, index) => ({
  row_slot: index + 39,
  installment_count: '',
  periodicity: '',
  start_month: '',
  installment_value: '',
  percent: '',
  total_vgv: '',
  adjustment_type: 'INCC',
  notes: '',
}));

const TODAY = new Date().toISOString().split('T')[0];

const EMPTY_PRODUCT_CONTEXT = {
  enterprise_name: '',
  unit_code: '',
  product_unit_key: '',
  garage_code: '',
  private_area_m2: 0,
  analysis_date: TODAY,
  delivery_month: '',
  modification_kind: 'Não',
  decorated_value_per_m2: null,
  facility_value_per_m2: null,
  area_for_modification_m2: 0,
  prize_enabled: true,
  fully_invoiced: false,
  has_permuta: false,
};

const EMPTY_COMMERCIAL_CONTEXT = {
  city_sales_manager_name: '',
  real_estate_name: '',
  broker_name: '',
  manager_name: '',
};

const EMPTY_COMMISSION_CONTEXT = {
  primary_commission_label: '',
  primary_commission_percent: 0,
  prize_commission_label: '',
  prize_commission_percent: 0,
  secondary_commission_slots: [
    { slot: 1, label: '', percent: null },
    { slot: 2, label: '', percent: null },
  ],
};

function cloneRows(rows = EMPTY_ROWS) {
  return rows.map((row) => ({ ...row }));
}

export function useScenarioState() {
  const [productContext, setProductContext] = useState(EMPTY_PRODUCT_CONTEXT);
  const [commercialContext, setCommercialContext] = useState(EMPTY_COMMERCIAL_CONTEXT);
  const [commissionContext, setCommissionContext] = useState(EMPTY_COMMISSION_CONTEXT);
  const [saleFlowRows, setSaleFlowRows] = useState(cloneRows());
  const [standardFlowRows, setStandardFlowRows] = useState(cloneRows());
  const [exchangeFlowRows, setExchangeFlowRows] = useState(cloneRows());
  const [scenarioMode, setScenarioMode] = useState('NORMAL');

  const updateProductContext = (field, value) => {
    setProductContext((current) => ({ ...current, [field]: value }));
  };

  const updateSaleRow = (index, field, value) => {
    setSaleFlowRows((current) => {
      const next = [...current];
      next[index] = { ...next[index], [field]: value };
      return next;
    });
  };

  const updateExchangeRow = (index, field, value) => {
    setExchangeFlowRows((current) => {
      const next = [...current];
      next[index] = { ...next[index], [field]: value };
      return next;
    });
  };

  const resetScenarioData = () => {
    setCommercialContext(EMPTY_COMMERCIAL_CONTEXT);
    setCommissionContext(EMPTY_COMMISSION_CONTEXT);
    setSaleFlowRows(cloneRows());
    setStandardFlowRows(cloneRows());
    setExchangeFlowRows(cloneRows());
  };

  const clearUnitSelection = (enterpriseName = '') => {
    setProductContext((current) => ({
      ...EMPTY_PRODUCT_CONTEXT,
      enterprise_name: enterpriseName,
      analysis_date: current.analysis_date || TODAY,
      has_permuta: current.has_permuta,
    }));
    resetScenarioData();
  };

  const applyUnitDefaults = (defaults, hasPermuta = false) => {
    const context = defaults?.product_context || {};
    setProductContext({
      enterprise_name: context.enterprise_name || '',
      unit_code: context.unit_code || '',
      product_unit_key: context.product_unit_key || '',
      garage_code: context.garage_code || '',
      private_area_m2: context.private_area_m2 || 0,
      analysis_date: context.default_analysis_date || TODAY,
      delivery_month: context.delivery_month || '',
      modification_kind: context.default_modification_kind || 'Não',
      decorated_value_per_m2: context.default_decorated_value_per_m2 ?? null,
      facility_value_per_m2: context.default_facility_value_per_m2 ?? null,
      area_for_modification_m2: context.default_area_for_modification_m2 || 0,
      prize_enabled: Boolean(context.default_prize_enabled),
      fully_invoiced: Boolean(context.default_fully_invoiced),
      has_permuta: hasPermuta,
    });
    setCommercialContext(defaults?.commercial_context || EMPTY_COMMERCIAL_CONTEXT);
    setCommissionContext(defaults?.commission_context || EMPTY_COMMISSION_CONTEXT);
    // O fluxo padrão é salvo em duas cópias:
    // standadFlowRows: imutável, serve como referência padrão
    // saleFlowRows: editável pelo usuário
    const defaultRows = defaults?.default_sale_flow_rows || EMPTY_ROWS;
    setStandardFlowRows(cloneRows(defaultRows));
    setSaleFlowRows(cloneRows(defaultRows));
    setExchangeFlowRows(cloneRows(defaults?.default_exchange_flow_rows || EMPTY_ROWS));
  };

  return {
    scenarioMode,
    setScenarioMode,
    productContext,
    setProductContext,
    updateProductContext,
    commercialContext,
    setCommercialContext,
    commissionContext,
    setCommissionContext,
    saleFlowRows,
    setSaleFlowRows,
    updateSaleRow,
    standardFlowRows,
    exchangeFlowRows,
    setExchangeFlowRows,
    updateExchangeRow,
    clearUnitSelection,
    applyUnitDefaults,
    resetScenarioData,
  };
}
