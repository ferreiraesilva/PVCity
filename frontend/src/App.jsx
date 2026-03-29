import { useEffect, useMemo, useState } from 'react';
import {
  ArrowRightLeft,
  Building2,
  Calculator,
  ChevronDown,
  Database,
  FileSpreadsheet,
  Home,
} from 'lucide-react';
import { clsx } from 'clsx';

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
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [referenceData, setReferenceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [screenError, setScreenError] = useState('');

  // Keyboard shortcut: Alt + B to toggle sidebar
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.altKey && e.key === 'b') {
        setIsSidebarCollapsed(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

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
        <aside 
          className={clsx(
            "hidden h-full flex-shrink-0 flex-col justify-between overflow-hidden py-7 text-white transition-all duration-300 xl:flex",
            isSidebarCollapsed ? "w-[76px] px-2 items-center" : "w-[260px] px-6"
          )}
        >
          <div className="min-h-0 w-full overflow-hidden">
            <div className={clsx(
              "mb-10 flex items-center gap-4 transition-all",
              isSidebarCollapsed && "justify-center gap-0"
            )}>
              <div className="rounded-[18px] bg-[#2b2930] p-2.5 shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
                <Building2 className="h-6 w-6 text-city-blue" />
              </div>
              {!isSidebarCollapsed && (
                <div className="animate-in fade-in slide-in-from-left-2 duration-300">
                  <div className="city-kicker text-[10px] text-[#ffcf97]">City workspace</div>
                  <h1 className="text-xl font-bold tracking-tight text-white leading-tight">PVCity</h1>
                </div>
              )}
            </div>

            <nav className="flex flex-col gap-1.5">
              <button
                className={clsx(
                  "group relative flex cursor-pointer items-center gap-3 rounded-[16px] py-2.5 transition-all duration-200",
                  isSidebarCollapsed ? "justify-center px-0" : "px-4 text-left",
                  activeSection === 'simulation'
                    ? "bg-white/10 text-white"
                    : "text-[#cfbfab] hover:bg-white/[0.05] hover:text-white"
                )}
                onClick={openSimulation}
                title={isSidebarCollapsed ? "Simulação" : ""}
              >
                <span
                  className={clsx(
                    "absolute left-2.5 top-1/2 h-5 w-1 -translate-y-1/2 rounded-full bg-white transition-opacity",
                    activeSection === 'simulation' ? "opacity-100" : "opacity-0"
                  )}
                />
                <Calculator className={clsx("h-[18px] w-[18px]", activeSection === 'simulation' && "ml-2.5 transition-all")} />
                {!isSidebarCollapsed && <span className="text-sm font-medium">Simulação</span>}
              </button>

              <div className={clsx(
                "rounded-[20px] bg-white/[0.03] transition-all",
                isSidebarCollapsed ? "p-0.5" : "p-1.5"
              )}>
                <button
                  className={clsx(
                    "group relative flex w-full cursor-pointer items-center justify-between rounded-[16px] py-2.5 transition-all duration-200",
                    isSidebarCollapsed ? "justify-center px-0" : "px-4 text-left",
                    activeSection === 'admin'
                      ? "bg-white/10 text-white"
                      : "text-[#cfbfab] hover:bg-white/[0.05] hover:text-white"
                  )}
                  onClick={() => setIsSidebarCollapsed(false) || setAdminMenuOpen((current) => !current)}
                  title={isSidebarCollapsed ? "Cadastros" : ""}
                >
                  <span
                    className={clsx(
                      "absolute left-2.5 top-1/2 h-5 w-1 -translate-y-1/2 rounded-full bg-white transition-opacity",
                      activeSection === 'admin' ? "opacity-100" : "opacity-0"
                    )}
                  />
                  <div className={clsx("flex items-center gap-3", isSidebarCollapsed && "justify-center")}>
                    <Database className={clsx("h-[18px] w-[18px]", activeSection === 'admin' && "ml-2.5 transition-all")} />
                    {!isSidebarCollapsed && <span className="text-sm font-medium">Cadastros</span>}
                  </div>
                  {!isSidebarCollapsed && (
                    <ChevronDown className={`h-4 w-4 transition-transform ${adminMenuOpen ? 'rotate-180' : ''}`} />
                  )}
                </button>

                {adminMenuOpen && !isSidebarCollapsed ? (
                  <div className="mt-1 flex flex-col gap-1 pl-2">
                    {ADMIN_SUBMENU.map((item) => {
                      const isActive = activeSection === 'admin' && activeAdminItem === item.key;
                      return (
                        <button
                          key={item.key}
                          className={`relative flex cursor-pointer items-center rounded-[12px] px-6 py-2 text-left text-xs transition-all duration-200 ${
                            isActive
                              ? 'bg-[#f7f2ea]/10 text-[#f7f2ea]'
                              : 'text-[#8e8578] hover:bg-white/[0.04] hover:text-white'
                          }`}
                          onClick={() => openAdminItem(item.key)}
                        >
                          {item.label}
                        </button>
                      );
                    })}
                  </div>
                ) : null}
              </div>
            </nav>
          </div>

          <div className="px-1">
            <button
              onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
              className="flex h-10 w-full items-center justify-center rounded-xl bg-white/5 text-[#cfbfab] hover:bg-white/10 hover:text-white transition-colors"
              title={isSidebarCollapsed ? "Expandir" : "Recolher"}
            >
              {isSidebarCollapsed ? <ArrowRightLeft className="h-4 w-4" /> : (
                <div className="flex items-center gap-2 text-xs font-semibold">
                  <ArrowRightLeft className="h-4 w-4" />
                  <span>Recolher Menu (Alt + B)</span>
                </div>
              )}
            </button>
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
