// Servicio de autenticación que maneja automáticamente la renovación de tokens

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

class AuthService {
  constructor() {
    this.isRefreshing = false;
    this.failedQueue = [];
  }

  // Obtener el access token actual
  getAccessToken() {
    return localStorage.getItem('access_token');
  }

  // Obtener el refresh token
  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  }

  // Verificar si el usuario está autenticado
  isAuthenticated() {
    const accessToken = this.getAccessToken();
    const refreshToken = this.getRefreshToken();
    return !!(accessToken && refreshToken);
  }

  // Renovar el access token usando el refresh token
  async refreshAccessToken() {
    const refreshToken = this.getRefreshToken();
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (!response.ok) {
        throw new Error('Failed to refresh token');
      }

      const data = await response.json();
      
      // Actualizar los tokens en localStorage
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user', JSON.stringify(data.user));

      return data.access_token;
    } catch (error) {
      // Si falla la renovación, limpiar todo y redirigir al login
      this.logout();
      throw error;
    }
  }

  // Procesar la cola de peticiones fallidas después de renovar el token
  processQueue(error, token = null) {
    this.failedQueue.forEach(({ resolve, reject }) => {
      if (error) {
        reject(error);
      } else {
        resolve(token);
      }
    });
    
    this.failedQueue = [];
  }

  // Realizar una petición autenticada con renovación automática de token
  async authenticatedFetch(url, options = {}) {
    const accessToken = this.getAccessToken();
    
    if (!accessToken) {
      throw new Error('No access token available');
    }

    // Añadir el token de autorización a las cabeceras
    const authOptions = {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${accessToken}`,
      },
    };

    try {
      const response = await fetch(url, authOptions);
      
      // Si el token ha expirado (401), intentar renovarlo
      if (response.status === 401) {
        if (this.isRefreshing) {
          // Si ya se está renovando, esperar en la cola
          return new Promise((resolve, reject) => {
            this.failedQueue.push({ resolve, reject });
          }).then(token => {
            authOptions.headers['Authorization'] = `Bearer ${token}`;
            return fetch(url, authOptions);
          });
        }

        this.isRefreshing = true;

        try {
          const newToken = await this.refreshAccessToken();
          this.processQueue(null, newToken);
          
          // Reintentar la petición original con el nuevo token
          authOptions.headers['Authorization'] = `Bearer ${newToken}`;
          return fetch(url, authOptions);
        } catch (refreshError) {
          this.processQueue(refreshError, null);
          throw refreshError;
        } finally {
          this.isRefreshing = false;
        }
      }

      return response;
    } catch (error) {
      throw error;
    }
  }

  // Cerrar sesión
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    
    // Opcional: notificar al servidor sobre el logout
    const accessToken = this.getAccessToken();
    if (accessToken) {
      fetch(`${API_BASE_URL}/api/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      }).catch(() => {
        // Ignorar errores del logout en el servidor
      });
    }
  }

  // Obtener información del usuario actual
  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  // Verificar si el token está próximo a expirar y renovarlo preventivamente
  async checkAndRefreshToken() {
    const accessToken = this.getAccessToken();
    
    if (!accessToken) {
      return false;
    }

    try {
      // Decodificar el token para verificar la expiración
      const payload = JSON.parse(atob(accessToken.split('.')[1]));
      const currentTime = Date.now() / 1000;
      
      // Si el token expira en menos de 5 minutos, renovarlo
      if (payload.exp - currentTime < 300) {
        await this.refreshAccessToken();
        return true;
      }
      
      return true;
    } catch (error) {
      // Si hay error al decodificar, intentar renovar
      try {
        await this.refreshAccessToken();
        return true;
      } catch (refreshError) {
        return false;
      }
    }
  }
}

// Exportar una instancia singleton
export default new AuthService();

