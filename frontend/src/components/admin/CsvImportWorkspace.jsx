import { useState } from 'react';
import { FileUp, Upload } from 'lucide-react';

import { services } from '../../api/services';
import { Button } from '../shared/Button';
import { Card } from '../shared/Card';
import { Input } from '../shared/Input';
import { Select } from '../shared/Select';
import { RESOURCE_CONFIG } from './adminConfig';


export function CsvImportWorkspace({ defaultResource = 'enterprises', onReferenceDataRefresh, onAfterImport }) {
  const [resource, setResource] = useState(defaultResource);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function handlePreviewImport() {
    if (!file) {
      setError('Selecione um arquivo CSV antes do preview.');
      return;
    }

    try {
      setBusy(true);
      setError('');
      const nextPreview = await services.previewImport(resource, file);
      setPreview(nextPreview);
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Falha ao validar o CSV.');
    } finally {
      setBusy(false);
    }
  }

  async function handleCommitImport() {
    if (!file) {
      setError('Selecione um arquivo CSV antes da importação.');
      return;
    }

    try {
      setBusy(true);
      setError('');
      const result = await services.commitImport(resource, file);
      setPreview((current) => ({ ...current, commit_result: result }));
      await onReferenceDataRefresh();
      onAfterImport?.(resource);
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Falha ao importar o CSV.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="grid grid-cols-1 gap-6 xl:grid-cols-12">
      <section className="xl:col-span-7">
        <Card>
          <div className="mb-4">
            <div className="city-kicker mb-1 text-[#b27619]">Rotina independente</div>
            <h2 className="text-lg font-semibold text-city-blue-dark">Importação CSV</h2>
            <p className="mt-1 text-sm text-text-muted">
              Execute a carga em lote de um cadastro por vez, com preview e commit separados.
            </p>
          </div>

          {error ? (
            <div className="mb-4 rounded-[18px] border border-danger-red/30 bg-danger-red/10 px-4 py-3 text-sm text-danger-red">
              {error}
            </div>
          ) : null}

          <div className="flex flex-col gap-4">
            <Select
              label="Cadastro"
              value={resource}
              options={Object.entries(RESOURCE_CONFIG).map(([value, config]) => ({
                value,
                label: config.title,
              }))}
              onChange={(event) => {
                setResource(event.target.value);
                setPreview(null);
              }}
            />
            <Input
              label="Arquivo CSV"
              type="file"
              accept=".csv"
              onChange={(event) => {
                setFile(event.target.files?.[0] || null);
                setPreview(null);
              }}
            />
            <div className="flex gap-3">
              <Button type="button" variant="outline" onClick={handlePreviewImport} disabled={busy}>
                <FileUp className="mr-2 h-4 w-4" />
                {busy ? 'Validando...' : 'Preview'}
              </Button>
              <Button type="button" onClick={handleCommitImport} disabled={busy || !preview?.can_commit}>
                <Upload className="mr-2 h-4 w-4" />
                Importar
              </Button>
            </div>
          </div>
        </Card>
      </section>

      <aside className="flex flex-col gap-6 xl:col-span-5">
        <Card>
          <h3 className="text-lg font-semibold text-city-blue-dark">Resultado do processamento</h3>
          {!preview ? (
            <div className="mt-4 rounded-[18px] border border-border-color bg-[#fffaf3] p-4 text-sm text-text-muted">
              Nenhum preview executado ainda.
            </div>
          ) : (
            <div className="mt-4 space-y-3 text-sm">
              <div className="rounded-[18px] bg-[#fff4e4] p-4 text-text-main">
                <div>Creates: {preview.summary.create}</div>
                <div>Updates: {preview.summary.update}</div>
                <div>Rejects: {preview.summary.reject}</div>
              </div>
              <div className="max-h-96 overflow-auto rounded-[18px] border border-[#eadfcf]">
                <table className="min-w-full divide-y divide-[#ece3d8] text-xs">
                  <thead>
                    <tr className="text-left text-text-muted">
                      <th className="px-3 py-2">Linha</th>
                      <th className="px-3 py-2">Ação</th>
                      <th className="px-3 py-2">Chave</th>
                      <th className="px-3 py-2">Erros</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#f1e7db]">
                    {preview.items.map((item) => (
                      <tr key={`${item.line_number}-${item.natural_key}`}>
                        <td className="px-3 py-2">{item.line_number}</td>
                        <td className="px-3 py-2">{item.action}</td>
                        <td className="px-3 py-2">{item.natural_key}</td>
                        <td className="px-3 py-2">{item.errors.length ? item.errors.join(' | ') : '--'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {preview.commit_result ? (
                <div className="rounded-[18px] border border-emerald-200 bg-emerald-50 p-4 text-xs text-emerald-900">
                  Importação concluída. Criados: {preview.commit_result.summary.created}, atualizados: {preview.commit_result.summary.updated}, rejeitados: {preview.commit_result.summary.rejected}
                </div>
              ) : null}
            </div>
          )}
        </Card>
      </aside>
    </div>
  );
}
