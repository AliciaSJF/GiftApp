import { useState, FormEvent } from 'react';
import './AuthModal.css';
import { authService, LoginCredentials, RegisterData } from '../services/authService';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

const AuthModal = ({ isOpen, onClose, onSuccess }: AuthModalProps) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      if (isLogin) {
        // Login
        const credentials: LoginCredentials = {
          username: username || email, // Permitir login con email o username
          password,
        };
        await authService.login(credentials);
        onSuccess?.();
        onClose();
        // Limpiar formulario
        setEmail('');
        setUsername('');
        setPassword('');
      } else {
        // Register
        if (!username || !email) {
          setError('El nombre de usuario y email son requeridos');
          setIsLoading(false);
          return;
        }
        const registerData: RegisterData = {
          email,
          username,
          password,
        };
        await authService.register(registerData);
        // Después de registrarse, hacer login automático
        await authService.login({ username, password });
        onSuccess?.();
        onClose();
        // Limpiar formulario
        setEmail('');
        setUsername('');
        setPassword('');
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Ocurrió un error. Por favor, intenta de nuevo.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleAuth = () => {
    try {
      authService.startGoogleOAuth();
    } catch (err) {
      setError('Error al iniciar autenticación con Google');
    }
  };

  const switchMode = () => {
    setIsLogin(!isLogin);
    setError(null);
    setEmail('');
    setUsername('');
    setPassword('');
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose} aria-label="Cerrar">
          ×
        </button>
        
        <div className="modal-header">
          <h2>{isLogin ? 'Iniciar sesión' : 'Crear cuenta'}</h2>
          <p>
            {isLogin 
              ? 'Accede a tu cuenta para continuar' 
              : 'Crea una cuenta para empezar'}
          </p>
        </div>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {/* Botón de Google OAuth */}
        <button
          type="button"
          className="btn-google"
          onClick={handleGoogleAuth}
          disabled={isLoading}
        >
          <svg className="google-icon" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Continuar con Google
        </button>

        <div className="divider">
          <span>o</span>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {!isLogin && (
            <div className="form-group">
              <label htmlFor="username">Nombre de usuario</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required={!isLogin}
                placeholder="tu_usuario"
                disabled={isLoading}
              />
            </div>
          )}

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required={!isLogin}
                placeholder="tu@email.com"
                disabled={isLoading}
              />
            </div>
          )}

          {isLogin && (
            <div className="form-group">
              <label htmlFor="login-identifier">Usuario o Email</label>
              <input
                type="text"
                id="login-identifier"
                value={username || email}
                onChange={(e) => {
                  const value = e.target.value;
                  // Detectar si es email o username
                  if (value.includes('@')) {
                    setEmail(value);
                    setUsername('');
                  } else {
                    setUsername(value);
                    setEmail('');
                  }
                }}
                required
                placeholder="usuario o email"
                disabled={isLoading}
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              disabled={isLoading}
              minLength={6}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="loading-spinner"></span>
            ) : (
              isLogin ? 'Iniciar sesión' : 'Crear cuenta'
            )}
          </button>
        </form>

        <div className="modal-footer">
          <p>
            {isLogin ? '¿No tienes cuenta? ' : '¿Ya tienes cuenta? '}
            <button
              type="button"
              className="link-button"
              onClick={switchMode}
              disabled={isLoading}
            >
              {isLogin ? 'Regístrate' : 'Inicia sesión'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthModal;
