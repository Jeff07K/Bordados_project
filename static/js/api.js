/**
 * api.js — Capa centralizada para llamadas a la API de Bordados.
 * Maneja tokens JWT automáticamente.
 */

const API_BASE = '';  // Misma URL (FastAPI sirve el frontend)

const Api = {
  // ── Token ─────────────────────────────────────────────────────
  getToken: () => localStorage.getItem('token'),
  setToken: (t) => localStorage.setItem('token', t),
  removeToken: () => localStorage.removeItem('token'),

  getUser: () => {
    try { return JSON.parse(localStorage.getItem('user') || 'null'); } 
    catch { return null; }
  },
  setUser: (u) => localStorage.setItem('user', JSON.stringify(u)),
  removeUser: () => localStorage.removeItem('user'),

  logout: () => {
    Api.removeToken();
    Api.removeUser();
    window.location.href = '/login';
  },

  isLoggedIn: () => !!Api.getToken(),
  isAdmin: () => Api.getUser()?.rol === 'admin',

  // ── Fetch base ─────────────────────────────────────────────────
  async _fetch(url, options = {}) {
    const token = Api.getToken();
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch(API_BASE + url, { ...options, headers });

    if (res.status === 401) {
      Api.logout();
      return;
    }

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      const msg = data?.detail || `Error ${res.status}`;
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }
    return data;
  },

  get: (url) => Api._fetch(url),
  post: (url, body) => Api._fetch(url, { method: 'POST', body: JSON.stringify(body) }),
  patch: (url, body) => Api._fetch(url, { method: 'PATCH', body: JSON.stringify(body) }),
  delete: (url) => Api._fetch(url, { method: 'DELETE' }),

  // ── Auth ───────────────────────────────────────────────────────
  async login(email, password) {
    const form = new URLSearchParams({ username: email, password });
    const res = await fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form,
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Error de login');
    Api.setToken(data.access_token);
    Api.setUser({ email, rol: data.rol, nombre: data.nombre });
    return data;
  },

  async register(payload) {
    return Api.post('/auth/register', payload);
  },

  // ── Productos ──────────────────────────────────────────────────
  getProductos: (soloActivos = true, categoria = '') =>
    Api.get(`/producto/?solo_activos=${soloActivos}${categoria ? `&categoria=${categoria}` : ''}`),

  getProducto: (id) => Api.get(`/producto/${id}`),
  createProducto: (data) => Api.post('/producto/', data),
  updateProducto: (id, data) => Api.patch(`/producto/${id}`, data),
  deleteProducto: (id) => Api.delete(`/producto/${id}`),

  // ── Pedidos ────────────────────────────────────────────────────
  getMisPedidos: () => Api.get('/pedido/mis-pedidos'),
  getAllPedidos: (estado = '') =>
    Api.get(`/pedido/${estado ? `?estado=${estado}` : ''}`),
  createPedido: (data) => Api.post('/pedido/', data),
  updatePedido: (id, data) => Api.patch(`/pedido/${id}`, data),
  cancelPedido: (id) => Api.delete(`/pedido/${id}`),

  // ── Usuarios (admin) ───────────────────────────────────────────
  getUsuarios: () => Api.get('/usuario/'),
  getMe: () => Api.get('/usuario/me'),
  updateMe: (data) => Api.patch('/usuario/me', data),
  deactivateUser: (id) => Api.delete(`/usuario/${id}`),
};

// Redirigir si no hay token (para páginas protegidas)
function requireAuth() {
  if (!Api.isLoggedIn()) { window.location.href = '/login'; }
}
function requireAdmin() {
  requireAuth();
  if (!Api.isAdmin()) { window.location.href = '/dashboard'; }
}

// Actualizar navbar según estado de sesión
function updateNavbar() {
  const user = Api.getUser();
  const logoutBtn = document.getElementById('nav-logout');
  const loginLink = document.getElementById('nav-login');
  const dashLink = document.getElementById('nav-dashboard');
  const adminLink = document.getElementById('nav-admin');

  if (user) {
    if (logoutBtn) logoutBtn.style.display = 'inline-flex';
    if (loginLink) loginLink.style.display = 'none';
    if (dashLink) dashLink.style.display = 'inline';
    if (adminLink && user.rol === 'admin') adminLink.style.display = 'inline';
  }
}
