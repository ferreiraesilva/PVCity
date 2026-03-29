import { useEffect, useMemo, useState } from 'react';
import { Database, Pencil, Plus, Trash2 } from 'lucide-react';

import { services } from '../../api/services';
import { Button } from '../shared/Button';
import { Card } from '../shared/Card';
import { Input } from '../shared/Input';
import { Select } from '../shared/Select';
import { RESOURCE_CONFIG, YES_NO_OPTIONS, normalizeValue, renderCell } from './adminConfig';


export function AdminCrudWorkspace({ resource, referenceData, onReferenceDataRefresh }) {
  const currentConfig = RESOURCE_CONFIG[resource];
  const [enterpriseRows, setEnterpriseRows] = useState([]);
  const [resourceRows, setResourceRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [formState, setFormState] = useState(currentConfig.empty);

  const enterpriseMap = useMemo(() => {
    const map = new Map();
    enterpriseRows.forEach((row) => {
      if (row.id && row.name) {
        map.set(row.id, row.name);
      }
    });
    return map;
  }, [enterpriseRows]);

  const enterpriseOptions = useMemo(() => {
    return enterpriseRows.map((row) => ({ label: row.name, value: String(row.id) }));
  }, [enterpriseRows]);

  const periodicityOptions = useMemo(() => {
    return (referenceData?.enums?.periodicity || []).map((value) => ({ label: value, value }));
  }, [referenceData]);

  useEffect(() => {
    setFormState(currentConfig.empty);
    setEditingId(null);
    setError('');
    loadResource(resource);
  }, [resource]);

  useEffect(() => {
    loadEnterprises();
  }, []);

  async function loadResource(nextResource) {
    try {
      setLoading(true);
      const rows = await services.listAdminResource(nextResource);
      setResourceRows(rows);
    } catch (requestError) {
      const message = requestError.code === 'ECONNABORTED'
        ? 'Erro operacional: timeout ao carregar dados do cadastro.'
        : 'Não foi possível carregar o cadastro selecionado.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  async function loadEnterprises() {
    try {
      const rows = await services.listAdminResource('enterprises');
      setEnterpriseRows(rows);
    } catch (requestError) {
      setError('Não foi possível carregar os empreendimentos para o backoffice.');
    }
  }

  function handleFormChange(fieldName, value) {
    setFormState((current) => ({ ...current, [fieldName]: value }));
  }

  function handleEdit(row) {
    setEditingId(row.id);
    setFormState({
      ...currentConfig.empty,
      ...row,
      enterprise_id: row.enterprise_id ? String(row.enterprise_id) : '',
    });
  }

  function resetForm() {
    setEditingId(null);
    setFormState(currentConfig.empty);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      setSaving(true);
      setError('');
      const payload = {};
      currentConfig.fields.forEach((field) => {
        payload[field.name] = normalizeValue(field, formState[field.name]);
      });

      if (editingId) {
        await services.updateAdminResource(resource, editingId, payload);
      } else {
        await services.createAdminResource(resource, payload);
      }
      resetForm();
      await loadResource(resource);
      await loadEnterprises();
      await onReferenceDataRefresh();
    } catch (requestError) {
      const message = requestError.code === 'ECONNABORTED'
        ? 'Erro operacional: timeout ao salvar. O servidor demorou muito a responder.'
        : (requestError.response?.data?.detail || 'Não foi possível salvar o cadastro.');
      setError(message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Confirma a exclusão deste registro?')) {
      return;
    }
    try {
      setError('');
      await services.deleteAdminResource(resource, id);
      if (editingId === id) {
        resetForm();
      }
      await loadResource(resource);
      await loadEnterprises();
      await onReferenceDataRefresh();
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Não foi possível remover o registro.');
    }
  }

  function getFieldOptions(field) {
    if (field.type === 'boolean') {
      return YES_NO_OPTIONS;
    }
    if (field.source === 'periodicity') {
      return periodicityOptions;
    }
    if (field.source === 'enterprises') {
      return enterpriseOptions;
    }
    return [];
  }

  return (
    <div className="grid grid-cols-1 gap-6 xl:grid-cols-12">
      <section className="xl:col-span-8">
        <Card>
          <div className="mb-6">
            <div className="city-kicker mb-1 text-[#b27619]">Rotina independente</div>
            <h2 className="text-lg font-semibold text-city-blue-dark">{currentConfig.title}</h2>
            <p className="mt-1 text-sm text-text-muted">{currentConfig.description}</p>
          </div>

          {error ? (
            <div className="mb-4 rounded-[18px] border border-danger-red/30 bg-danger-red/10 px-4 py-3 text-sm text-danger-red">
              {error}
            </div>
          ) : null}

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-[#ece3d8] text-sm">
              <thead>
                <tr className="text-left text-text-muted">
                  {currentConfig.columns.map((column) => (
                    <th key={column} className="px-3 py-2 font-medium">
                      {column}
                    </th>
                  ))}
                  <th className="px-3 py-2 font-medium">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#f1e7db]">
                {loading ? (
                  <tr>
                    <td className="px-3 py-4 text-text-muted" colSpan={currentConfig.columns.length + 1}>
                      Carregando...
                    </td>
                  </tr>
                ) : null}
                {!loading && resourceRows.length === 0 ? (
                  <tr>
                    <td className="px-3 py-4 text-text-muted" colSpan={currentConfig.columns.length + 1}>
                      Nenhum registro cadastrado.
                    </td>
                  </tr>
                ) : null}
                {!loading
                  ? resourceRows.map((row) => (
                      <tr key={row.id}>
                        {currentConfig.columns.map((column) => (
                          <td key={`${row.id}-${column}`} className="px-3 py-3 text-text-main">
                            {renderCell(column, row, enterpriseMap)}
                          </td>
                        ))}
                        <td className="px-3 py-3">
                          <div className="flex gap-2">
                            <Button variant="outline" className="px-3 py-2" onClick={() => handleEdit(row)}>
                              <Pencil className="h-4 w-4" />
                            </Button>
                            <Button variant="outline" className="px-3 py-2" onClick={() => handleDelete(row.id)}>
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))
                  : null}
              </tbody>
            </table>
          </div>
        </Card>
      </section>

      <aside className="flex flex-col gap-6 xl:col-span-4">
        <Card>
          <div className="mb-4 flex items-center gap-2">
            <Database className="h-5 w-5 text-city-blue" />
            <h3 className="text-lg font-semibold text-city-blue-dark">
              {editingId ? 'Editar registro' : 'Novo registro'}
            </h3>
          </div>
          <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
            {currentConfig.fields.map((field) => {
              if (field.type === 'select' || field.type === 'boolean') {
                return (
                  <Select
                    key={field.name}
                    label={field.label}
                    value={formState[field.name] ?? ''}
                    options={getFieldOptions(field)}
                    onChange={(event) => handleFormChange(field.name, event.target.value)}
                  />
                );
              }

              return (
                <Input
                  key={field.name}
                  label={field.label}
                  type={field.type === 'number' ? 'number' : 'text'}
                  step={field.type === 'number' ? 'any' : undefined}
                  value={formState[field.name] ?? ''}
                  onChange={(event) => handleFormChange(field.name, event.target.value)}
                />
              );
            })}
            <div className="flex gap-3">
              <Button type="submit" disabled={saving}>
                <Plus className="mr-2 h-4 w-4" />
                {saving ? 'Salvando...' : editingId ? 'Salvar alterações' : 'Criar registro'}
              </Button>
              <Button type="button" variant="secondary" onClick={resetForm}>
                Limpar
              </Button>
            </div>
          </form>
        </Card>
      </aside>
    </div>
  );
}
