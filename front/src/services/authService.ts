/**
 * Servicio de autenticación
 */
import apiClient from './api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  username?: string;
  display_name?: string;
  avatar_url?: string;
  is_active: boolean;
}

class AuthService {
  /**
   * Inicia sesión con usuario y contraseña
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>(
      '/users/login',
      credentials
    );
    
    // Guardar token en localStorage
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    
    return response.data;
  }

  /**
   * Registra un nuevo usuario
   */
  async register(data: RegisterData): Promise<User> {
    const response = await apiClient.post<User>('/users/', data);
    return response.data;
  }

  /**
   * Inicia el flujo de OAuth con Google
   */
  startGoogleOAuth(): void {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const apiBasePath = import.meta.env.VITE_API_BASE_PATH || '';
    const oauthUrl = `${apiUrl}${apiBasePath}/auth/oauth/google/start`;
    
    // Redirigir a la URL de OAuth
    window.location.href = oauthUrl;
  }

  /**
   * Maneja el callback de OAuth (se llama después de la redirección)
   */
  async handleOAuthCallback(token: string): Promise<void> {
    if (token) {
      localStorage.setItem('access_token', token);
    }
  }

  /**
   * Cierra sesión
   */
  logout(): void {
    localStorage.removeItem('access_token');
    window.location.href = '/';
  }

  /**
   * Verifica si el usuario está autenticado
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  /**
   * Obtiene el token de acceso
   */
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Obtiene el usuario actual
   * TODO: Implementar endpoint /users/me en el backend
   */
  // async getCurrentUser(): Promise<User> {
  //   const response = await apiClient.get<User>('/users/me');
  //   return response.data;
  // }
}

export const authService = new AuthService();

