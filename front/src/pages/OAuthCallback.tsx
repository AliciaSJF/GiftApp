import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { authService } from '../services/authService';
import './OAuthCallback.css';

const OAuthCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Procesando autenticación...');

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const token = searchParams.get('token');
        const error = searchParams.get('error');

        if (error) {
          setStatus('error');
          setMessage('Error en la autenticación. Por favor, intenta de nuevo.');
          setTimeout(() => {
            navigate('/');
          }, 3000);
          return;
        }

        if (token) {
          await authService.handleOAuthCallback(token);
          setStatus('success');
          setMessage('¡Autenticación exitosa! Redirigiendo...');
          setTimeout(() => {
            navigate('/');
          }, 1500);
        } else {
          setStatus('error');
          setMessage('No se recibió el token de autenticación.');
          setTimeout(() => {
            navigate('/');
          }, 3000);
        }
      } catch (error) {
        setStatus('error');
        setMessage('Error al procesar la autenticación. Por favor, intenta de nuevo.');
        setTimeout(() => {
          navigate('/');
        }, 3000);
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  return (
    <div className="oauth-callback">
      <div className="oauth-callback-content">
        {status === 'loading' && (
          <>
            <div className="spinner"></div>
            <p>{message}</p>
          </>
        )}
        {status === 'success' && (
          <>
            <div className="success-icon">✓</div>
            <p>{message}</p>
          </>
        )}
        {status === 'error' && (
          <>
            <div className="error-icon">✕</div>
            <p>{message}</p>
          </>
        )}
      </div>
    </div>
  );
};

export default OAuthCallback;

