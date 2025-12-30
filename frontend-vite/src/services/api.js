import axios from 'axios';

// API configuration - auto-detect based on environment
const getApiBaseUrl = () => {
    const hostname = window.location.hostname;
    const port = window.location.port;

    // If running through nginx proxy (production)
    if (port === '8081' && hostname !== 'localhost') {
        return `${window.location.protocol}//${hostname}:${port}/api`;
    }
    // Development mode
    else if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:8000/api';
    }
    // Docker or production environment
    else {
        return '/api';
    }
};

const API_BASE_URL = getApiBaseUrl();

const api = {
    async get(endpoint) {
        const response = await axios.get(`${API_BASE_URL}${endpoint}`);
        return response.data;
    },

    async post(endpoint, data = null) {
        const response = await axios.post(`${API_BASE_URL}${endpoint}`, data);
        return response.data;
    }
};

export default api;
