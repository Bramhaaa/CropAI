import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const api = {
  // System Health
  async getHealth() {
    const response = await client.get('/health');
    return response.data;
  },

  // Disease Diagnosis
  async predictDisease(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);
    const response = await client.post('/api/v1/disease/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Crop Recommendation
  async recommendCrop(payload) {
    const response = await client.post('/api/v1/crop/recommend', payload);
    return response.data;
  },

  // Yield Prediction
  async predictYield(payload) {
    const response = await client.post('/api/v1/yield/predict', payload);
    return response.data;
  },
};

export default api;
