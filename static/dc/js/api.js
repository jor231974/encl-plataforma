// Configuracion de la API
const API_BASE = '/api';
// SI CAMBIA LA URL, actualiza la linea de arriba
// Para deploy permanente, usa: const API_BASE = 'https://tu-app.onrender.com/api';

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('auth_token');
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers, credentials: 'include' });
    if (!res.ok) {
        const err = await res.json().catch(() => ({ error: res.statusText }));
        throw new Error(err.error || 'Error de conexion');
    }
    return res.json();
}
