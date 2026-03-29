import { useEffect, useMemo, useState } from 'react';
import {
  Building2,
  Calculator,
  ChevronDown,
  Database,
  FileSpreadsheet,
  Home,
} from 'lucide-react';

import { services } from './api/services';
import { AdminCrudWorkspace } from './components/admin/AdminCrudWorkspace';
import { CsvImportWorkspace } from './components/admin/CsvImportWorkspace';
import { RESOURCE_CONFIG } from './components/admin/adminConfig';
import { SimulationWorkspace } from './components/simulation/SimulationWorkspace';


const ADMIN_SUBMENU = [
  { key: 'enterprises', label: 'Empreendimentos' },
  { key: 'units', label: 'Unidades' },
  { key: 'standard-flows', label: 'Fluxos padrão' },
  { key: 'real-estate-agencies', label: 'Imobiliárias' },
  { key: 'imports', label: 'Importações CSV' },
];


function App() {
  const [activeSection, setActiveSection] = useState('simulation');
  const [activeAdminItem, setActiveAdminItem] = useState('enterprises');
  const [adminMenuOpen, setAdminMenuOpen] = useState(true);
  const [referenceData, setReferenceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [screenError, setScreenError] = useState('');

  const pageMeta = useMemo(() => {
    if (activeSection === 'simulation') {
      return {
        title: 'Simulador de proposta',
        description:
          'Selecione empreendimento, unidade e data-base. O fluxo padrão é carregado antes da comparação entre PV padrão e PV da proposta.',
        badge: 'Módulo de análise',
      };
    }

    if (activeAdminItem === 'imports') {
      return {
        title: 'Importação operacional',
        description:
          'Faça a carga em lote com preview e commit separados, sem misturar esta rotina com os CRUDs de manutenção.',
        badge: 'Rotina de importação',
      };
    }

    return {
      title: RESOURCE_CONFIG[activeAdminItem].title,
      description: RESOURCE_CONFIG[activeAdminItem].description,
      badge: 'Rotina de manutenção',
    };
  }, [activeSection, activeAdminItem]);

  async function loadBootstrap() {
    try {
      setLoading(true);
      setScreenError('');
      const data = await services.getBootstrapData();
      setReferenceData(data);
    } catch (error) {
      const message = error.code === 'ECONNABORTED'
        ? 'Erro operacional: timeout no backend ou no banco.'
        : 'Não foi possível carregar os dados operacionais do sistema.';
      setScreenError(message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadBootstrap();
  }, []);

  function openSimulation() {
    setActiveSection('simulation');
  }

  function openAdminItem(itemKey) {
    setActiveSection('admin');
    setAdminMenuOpen(true);
    setActiveAdminItem(itemKey);
  }

  return (
    <div className="min-h-screen p-3 md:p-5">
      <div className="workspace-shell mx-auto flex h-[calc(100vh-1.5rem)] max-w-[1720px] overflow-hidden rounded-[34px]">
        <aside className="hidden h-full w-[320px] flex-shrink-0 flex-col justify-between overflow-hidden px-7 py-7 text-white xl:flex">
          <div className="min-h-0 overflow-hidden">
            <div className="mb-10 flex items-center gap-4">
              <div className="rounded-[22px] bg-[#2b2930] p-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
                <Building2 className="h-7 w-7 text-city-blue" />
              </div>
              <div>
                <div className="city-kicker text-[#ffcf97]">City workspace</div>
                <h1 className="text-2xl font-semibold tracking-[-0.03em] text-white">PVCity</h1>
              </div>
            </div>


            <nav className="flex flex-col gap-2">
              <button
                className={`group relative flex cursor-pointer items-center gap-3 rounded-[18px] px-4 py-3 text-left transition-all duration-200 ${
                  activeSection === 'simulation'
                    ? 'bg-white/10 text-white'
                    : 'text-[#cfbfab] hover:bg-white/[0.05] hover:text-white'
                }`}
                onClick={openSimulation}
              >
                <span
                  className={`absolute left-0 top-1/2 h-10 w-1.5 -translate-y-1/2 rounded-r-full bg-white transition-opacity ${
                    activeSection === 'simulation' ? 'opacity-100' : 'opacity-0'
                  }`}
                />
                <Calculator className="h-4 w-4" />
                <span className="text-sm font-medium">Simulação</span>
              </button>

              <div className="rounded-[22px] bg-white/[0.03] p-2">
                <button
                  className={`group relative flex w-full cursor-pointer items-center justify-between rounded-[18px] px-4 py-3 text-left transition-all duration-200 ${
                    activeSection === 'admin'
                      ? 'bg-white/10 text-white'
                      : 'text-[#cfbfab] hover:bg-white/[0.05] hover:text-white'
                  }`}
                  onClick={() => setAdminMenuOpen((current) => !current)}
                >
                  <span
                    className={`absolute left-0 top-1/2 h-10 w-1.5 -translate-y-1/2 rounded-r-full bg-white transition-opacity ${
                      activeSection === 'admin' ? 'opacity-100' : 'opacity-0'
                    }`}
                  />
                  <div className="flex items-center gap-3">
                    <Database className="h-4 w-4" />
                    <span className="text-sm font-medium">Cadastros</span>
                  </div>
                  <ChevronDown className={`h-4 w-4 transition-transform ${adminMenuOpen ? 'rotate-180' : ''}`} />
                </button>

                {adminMenuOpen ? (
                  <div className="mt-2 flex flex-col gap-1 pl-4">
                    {ADMIN_SUBMENU.map((item) => {
                      const isActive = activeSection === 'admin' && activeAdminItem === item.key;
                      return (
                        <button
                          key={item.key}
                          className={`relative flex cursor-pointer items-center rounded-[16px] px-4 py-2.5 text-left text-sm transition-all duration-200 ${
                            isActive
                              ? 'bg-[#f7f2ea] text-[#212026]'
                              : 'text-[#c6b7a3] hover:bg-white/[0.06] hover:text-white'
                          }`}
                          onClick={() => openAdminItem(item.key)}
                        >
                          <span
                            className={`absolute left-0 top-1/2 h-8 w-1.5 -translate-y-1/2 rounded-r-full bg-white transition-opacity ${
                              isActive ? 'opacity-100' : 'opacity-0'
                            }`}
                          />
                          {item.label}
                        </button>
                      );
                    })}
                  </div>
                ) : null}
              </div>
            </nav>
          </div>

        </aside>

        <section className="workspace-panel m-2.5 flex min-w-0 flex-1 flex-col overflow-hidden rounded-[30px] md:m-3.5">
          <div className="border-b border-border-color/80 px-5 py-5 md:px-8 md:py-7">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <div className="mb-2 flex items-center gap-2 text-sm text-text-muted">
                  <Home className="h-4 w-4" />
                  <span>Aplicação operacional City</span>
                  {activeSection === 'admin' ? (
                    <>
                      <span>•</span>
                      <FileSpreadsheet className="h-4 w-4" />
                      <span>{pageMeta.title}</span>
                    </>
                  ) : null}
                </div>
                <h2 className="text-3xl font-semibold text-text-main md:text-4xl">{pageMeta.title}</h2>
                <p className="mt-3 max-w-3xl text-sm leading-6 text-text-muted md:text-base">
                  {pageMeta.description}
                </p>
              </div>
              <div className="rounded-full border border-[#e5d7c3] bg-white/80 px-4 py-2 text-sm text-text-muted">
                {pageMeta.badge}
              </div>
            </div>
          </div>

          <div className="min-h-0 flex-1 overflow-y-auto px-4 py-4 md:px-6 md:py-6">
            {screenError ? (
              <div className="mb-6 rounded-[22px] border border-danger-red/25 bg-[#fff3f2] px-5 py-4 text-sm text-danger-red">
                {screenError}
              </div>
            ) : null}

            {loading ? (
              <div className="card-panel rounded-[26px] px-6 py-10 text-text-muted">
                Carregando contexto operacional...
              </div>
            ) : null}

            {!loading && activeSection === 'simulation' ? (
              <SimulationWorkspace referenceData={referenceData} />
            ) : null}

            {!loading && activeSection === 'admin' && activeAdminItem !== 'imports' ? (
              <AdminCrudWorkspace
                resource={activeAdminItem}
                referenceData={referenceData}
                onReferenceDataRefresh={loadBootstrap}
              />
            ) : null}

            {!loading && activeSection === 'admin' && activeAdminItem === 'imports' ? (
              <CsvImportWorkspace
                defaultResource="enterprises"
                onReferenceDataRefresh={loadBootstrap}
                onAfterImport={(resourceKey) => setActiveAdminItem(resourceKey)}
              />
            ) : null}
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;
