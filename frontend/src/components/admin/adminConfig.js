export const YES_NO_OPTIONS = [
  { label: 'Sim', value: 'true' },
  { label: 'Não', value: 'false' },
];

export const RESOURCE_CONFIG = {
  enterprises: {
    title: 'Empreendimentos',
    description: 'Mantenha o cadastro mestre dos empreendimentos operacionais.',
    columns: ['name', 'city', 'discount_percent', 'vpl_rate_annual', 'is_active'],
    fields: [
      { name: 'name', label: 'Nome', type: 'text', required: true },
      { name: 'work_code', label: 'Código da obra', type: 'text' },
      { name: 'spe_name', label: 'SPE', type: 'text' },
      { name: 'city', label: 'Cidade', type: 'text' },
      { name: 'discount_percent', label: 'Desconto (%)', type: 'number' },
      { name: 'vpl_rate_annual', label: 'VPL anual', type: 'number' },
      { name: 'delivery_month', label: 'Entrega', type: 'text' },
      { name: 'launch_date', label: 'Lançamento', type: 'text' },
      { name: 'stage', label: 'Estágio', type: 'text' },
      { name: 'is_active', label: 'Ativo', type: 'boolean' },
    ],
    empty: {
      name: '',
      work_code: '',
      spe_name: '',
      city: '',
      discount_percent: 0,
      vpl_rate_annual: 0,
      delivery_month: '',
      launch_date: '',
      stage: '',
      is_active: true,
    },
  },
  units: {
    title: 'Unidades',
    description: 'Cadastre as unidades disponíveis dentro de cada empreendimento.',
    columns: ['enterprise_id', 'code', 'unit_type', 'private_area_m2', 'base_price', 'status'],
    fields: [
      { name: 'enterprise_id', label: 'Empreendimento', type: 'select', required: true, source: 'enterprises' },
      { name: 'code', label: 'Código', type: 'text', required: true },
      { name: 'product_unit_key', label: 'Chave produto/unidade', type: 'text' },
      { name: 'unit_type', label: 'Tipo', type: 'text' },
      { name: 'suites', label: 'Suítes', type: 'number' },
      { name: 'garage_code', label: 'Escaninho/Garagem', type: 'text' },
      { name: 'garage_spots', label: 'Vagas', type: 'number' },
      { name: 'private_area_m2', label: 'Área privativa (m²)', type: 'number' },
      { name: 'base_price', label: 'Preço base', type: 'number' },
      { name: 'status', label: 'Status', type: 'text' },
      { name: 'ideal_capture_percent', label: 'Captura ideal (%)', type: 'number' },
    ],
    empty: {
      enterprise_id: '',
      code: '',
      product_unit_key: '',
      unit_type: '',
      suites: '',
      garage_code: '',
      garage_spots: '',
      private_area_m2: 0,
      base_price: 0,
      status: '',
      ideal_capture_percent: 1,
    },
  },
  'standard-flows': {
    title: 'Fluxos Padrão',
    description: 'Defina o fluxo padrão por empreendimento sem misturar com outras rotinas.',
    columns: ['enterprise_id', 'row_slot', 'periodicity', 'installment_count', 'percent', 'installment_value'],
    fields: [
      { name: 'enterprise_id', label: 'Empreendimento', type: 'select', required: true, source: 'enterprises' },
      { name: 'row_slot', label: 'Slot da linha', type: 'number', required: true },
      { name: 'periodicity', label: 'Periodicidade', type: 'select', required: true, source: 'periodicity' },
      { name: 'installment_count', label: 'Quantidade', type: 'number' },
      { name: 'start_month', label: 'Início (mês)', type: 'number' },
      { name: 'percent', label: 'Percentual', type: 'number' },
      { name: 'installment_value', label: 'Valor parcela', type: 'number' },
    ],
    empty: {
      enterprise_id: '',
      row_slot: '',
      periodicity: '',
      installment_count: 1,
      start_month: '',
      percent: 0,
      installment_value: 0,
    },
  },
  'real-estate-agencies': {
    title: 'Imobiliárias',
    description: 'Gerencie as imobiliárias habilitadas para uso operacional.',
    columns: ['name', 'is_active'],
    fields: [
      { name: 'name', label: 'Nome', type: 'text', required: true },
      { name: 'is_active', label: 'Ativa', type: 'boolean' },
    ],
    empty: {
      name: '',
      is_active: true,
    },
  },
  'financial-params': {
    title: 'Parâmetros Financeiros',
    description: 'Configure as taxas globais e premissas financeiras que impactam o PV (VPL) de todas as simulações.',
  },
};

export function normalizeValue(field, value) {
  if (field.type === 'number') {
    return value === '' ? null : Number(value);
  }
  if (field.type === 'boolean') {
    return value === true || value === 'true';
  }
  if (field.type === 'select' && field.name === 'enterprise_id') {
    return value === '' ? null : Number(value);
  }
  return value === '' ? null : value;
}

export function renderCell(column, item, enterpriseMap) {
  const value = item[column];
  if (column === 'enterprise_id') {
    return enterpriseMap.get(value) || value || '--';
  }
  if (typeof value === 'boolean') {
    return value ? 'Sim' : 'Não';
  }
  if (value === null || value === undefined || value === '') {
    return '--';
  }
  return String(value);
}
