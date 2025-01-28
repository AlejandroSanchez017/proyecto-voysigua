import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "./LoginForm.css"
import { FaUser, FaLock } from "react-icons/fa";

function LoginForm({ onLogin }) {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Verificar credenciales de prueba (esto es solo un ejemplo)
    if (credentials.username === 'admin' && credentials.password === 'admin123') {
      onLogin(true);  // Cambiar el estado de autenticación
      navigate('/home');  // Redirigir a la página de AdminDashboard
    } else {
      alert('Credenciales incorrectas');
    }
  };

  return (
   <div className='login-form'>
    <div className="wrapper">
            <form onSubmit={handleSubmit}>
                <h1>Login</h1>
                <div className="input_box">
                    <input 
                        type="text" 
                        placeholder="Nombre de Usuario" 
                        value={credentials.username}
                        onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                        required 
                    />
                    <FaUser className="icon" />
                </div>
                <div className="input_box">
                    <input 
                        type="password" 
                        placeholder="Contraseña" 
                        value={credentials.password}
                        onChange={(e) => setCredentials({ ...credentials, password: e.target.value })} 
                        required 
                    />
                    <FaLock className="icon" />
                </div>
                
                <div className="remember-forgot">
                    <label><input type="checkbox" />Recordar</label>
                    <a href="/home">¿Olvidaste tu contraseña?</a>
                </div>
                <button type="submit">Ingresar</button>
            </form>
            </div>
        </div>
  );
}

export default LoginForm;
