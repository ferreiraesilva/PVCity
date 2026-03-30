import { apiClient } from './client';

export const services = {
  async getBootstrapData() {
    const { data } = await apiClient.get('/bootstrap/reference-data');
    return data;
  },

  async getUnitDefaults(enterpriseName, unitCode) {
    const { data } = await apiClient.get(`/products/${encodeURIComponent(enterpriseName)}/units/${encodeURIComponent(unitCode)}/defaults`);
    return data;
  },

  async calculateScenario(payload) {
    const { data } = await apiClient.post('/scenarios/calculate', payload);
    return data;
  },

  async listAdminResource(resource) {
    const { data } = await apiClient.get(`/admin/${resource}`);
    return data;
  },

  async createAdminResource(resource, payload) {
    const { data } = await apiClient.post(`/admin/${resource}`, payload);
    return data;
  },

  async updateAdminResource(resource, id, payload) {
    const { data } = await apiClient.put(`/admin/${resource}/${id}`, payload);
    return data;
  },

  async deleteAdminResource(resource, id) {
    await apiClient.delete(`/admin/${resource}/${id}`);
  },

  async previewImport(resource, file) {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await apiClient.post(`/admin/import/${resource}/preview`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },

  async commitImport(resource, file) {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await apiClient.post(`/admin/import/${resource}/commit`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },
  
  async updateConfig(key, value) {
    const { data } = await apiClient.put(`/admin/config/${key}`, { value });
    return data;
  },
};
