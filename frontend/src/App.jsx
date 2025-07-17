import { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import authService from './services/authService';
import './App.css';
import { Moon, Sun } from 'lucide-react';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [currentView, setCurrentView] = useState('login'); // 'login' or 'register'
  const [loading, setLoading] = useState(true);
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');

  useEffect(() => {
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(theme);
    localStorage.setItem('theme', theme);

    // Verificar si el usuario ya está autenticado
    checkAuthStatus();
  }, [theme]);

  const checkAuthStatus = async () => {
    try {
      if (authService.isAuthenticated()) {
        // Verificar y renovar el token si es necesario
        const isValid = await authService.checkAndRefreshToken();
        
        if (isValid) {
          const currentUser = authService.getCurrentUser();
          const currentToken = authService.getAccessToken();
          
          if (currentUser && currentToken) {
            setUser(currentUser);
            setToken(currentToken);
          }
        } else {
          // Si no se pudo renovar el token, limpiar la sesión
          authService.logout();
        }
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
      authService.logout();
    } finally {
      setLoading(false);
    }
  };

  // Configurar un intervalo para verificar y renovar tokens periódicamente
  useEffect(() => {
    if (user && token) {
      const interval = setInterval(async () => {
        try {
          await authService.checkAndRefreshToken();
          // Actualizar el token en el estado si se renovó
          const newToken = authService.getAccessToken();
          if (newToken !== token) {
            setToken(newToken);
          }
        } catch (error) {
          console.error('Error refreshing token:', error);
          handleLogout();
        }
      }, 5 * 60 * 1000); // Verificar cada 5 minutos

      return () => clearInterval(interval);
    }
  }, [user, token]);

  const handleLogin = (userData, userToken) => {
    setUser(userData);
    setToken(userToken);
  };

  const handleLogout = () => {
    authService.logout();
    setUser(null);
    setToken(null);
    setCurrentView('login');
  };

  const switchToRegister = () => {
    setCurrentView('register');
  };

  const switchToLogin = () => {
    setCurrentView('login');
  };

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background text-foreground">
      <button
        onClick={toggleTheme}
        className="absolute top-4 right-4 p-2 rounded-full bg-card text-card-foreground shadow-md"
      >
        {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
      </button>
      {user && token ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : currentView === 'register' ? (
        <Register onSwitchToLogin={switchToLogin} />
      ) : (
        <Login onLogin={handleLogin} onSwitchToRegister={switchToRegister} />
      )}

    </div>
  );
}

export default App;
