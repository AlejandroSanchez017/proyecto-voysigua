import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginForm.css";
import { FaUser, FaLock, FaEye, FaEyeSlash } from "react-icons/fa";

const LoginForm = ({onLogin}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  // Redirigir si el usuario ya tiene una sesión activa
 // useEffect(() => {
   // const token = sessionStorage.getItem("token");
    //if (token) {
      //navigate();
    //}
  //}, [navigate]);

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");

    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.status === 401) {
        throw new Error("Credenciales incorrectas");
      } else if (!response.ok) {
        throw new Error(data.detail || "Error en el inicio de sesión");
      }

      setMessage("Inicio de sesión exitoso");
      sessionStorage.setItem("token", data.access_token); // Usar sessionStorage en lugar de localStorage
      onLogin(true); 
      navigate('/home'); // Redireccionar al home
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="login-content-wrapper">
      <div className="login-card">
        <div className="header-image">
          <div className="circle-logo">VoySigua</div>
        </div>

        <form onSubmit={handleLogin}>
          <h1>Iniciar Sesión</h1>
          <div className="input_box">
            <input
              type="text"
              placeholder="Nombre de Usuario"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <FaUser className="icon" />
          </div>
          <div className="input_box">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <FaLock className="icon" />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="toggle-password"
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </button>
          </div>

          <div className="remember-forgot">
            <label>
              <input type="checkbox" /> Recordar
            </label>
            <a href="/forgot-password">¿Olvidaste tu contraseña?</a>
          </div>

          <button type="submit">Ingresar</button>

          {error && <p style={{ color: "red" }}>{error}</p>}
          {message && <p style={{ color: "green" }}>{message}</p>}

          <div className="signup-link">
            ¿No tienes una cuenta? <a href="/signup">Regístrate aquí</a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
