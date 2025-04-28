import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginForm.css";
import { FaUser, FaLock, FaEye, FaEyeSlash, FaKey } from "react-icons/fa";

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState(""); // Nuevo estado para OTP
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [step, setStep] = useState(1); // Controla si está en login o OTP
  const [tempToken, setTempToken] = useState(""); // Guarda el token antes de OTP

  const navigate = useNavigate();

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

      // Guardamos el token temporal y pasamos al paso 2 (OTP)
      setTempToken(data.temp_token);
      setStep(2);
      setMessage("Se ha enviado un código OTP a tu correo.");
    } catch (error) {
      setError(error.message);
    }
  };

  const handleVerifyOtp = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");

    try {
      const response = await fetch("http://localhost:8000/verify-otp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          otp_code: otp,
          temp_token: tempToken,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Error en la verificación del OTP");
      }

      // GUARDAR TOKEN, USERNAME, ROLES Y PERMISOS
      sessionStorage.setItem("token", data.access_token);
      sessionStorage.setItem("username", username);

      //  Guardar roles y permisos en localStorage (o sessionStorage si prefieres)
      localStorage.setItem("user_roles", JSON.stringify(data.user.roles));
      localStorage.setItem(
        "user_permissions",
        JSON.stringify(data.user.permissions)
      );

      setMessage("Autenticación exitosa");
      onLogin(true);
      navigate("/home");
    } catch (error) {
      setError(error.message);
    }
  };

  const handleResendOtp = async () => {
    try {
      const response = await fetch("http://localhost:8000/resend-otp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username }), // Se reutiliza el username ya ingresado
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Error al reenviar el código");
      }

      setMessage(data.message);
      setError(null);
    } catch (err) {
      setError(err.message);
      setMessage(null);
    }
  };

  return (
    <div className="login-content-wrapper">
      <div className="login-card">
        <div className="header-image">
          <div className="circle-logo">VoySigua</div>
        </div>

        {step === 1 ? (
          <form onSubmit={handleLogin}>
            <h1>Iniciar Sesión</h1>
            <div className="input_box password-input">
              <input
                type="text"
                placeholder=" Nombre de Usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
              <FaUser className="icon" />
            </div>
            <div className="input_box password-input">
  <input
    type={showPassword ? "text" : "password"}
    placeholder="Contraseña"
    value={password}
    onChange={(e) => setPassword(e.target.value)}
    required
  />
  <FaLock className="icon" aria-hidden="true" />
  <button
    type="button"
    onClick={() => setShowPassword(!showPassword)}
    className="toggle-password"
  >
    {showPassword ? <FaEyeSlash /> : <FaEye />}
  </button>
</div>

            <button type="submit">Ingresar</button>

            {error && <p style={{ color: "red" }}>{error}</p>}
            {message && <p style={{ color: "green" }}>{message}</p>}

            <div className="signup-link">
              ¿No tienes una cuenta? <a href="/nuevousuario">Regístrate aquí</a>
            </div>
          </form>
        ) : (
          <form onSubmit={handleVerifyOtp}>
            <h1>Verificación OTP</h1>
            <p>Introduce el código que enviamos a tu correo:</p>
            <div className="input_box password-input">
              <input
                type="text"
                placeholder="Código OTP"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                required
              />
              <FaKey className="icon" />
            </div>

            <button type="submit">Verificar OTP</button>
            <button
              type="button"
              onClick={handleResendOtp}
              className="resend-otp-button"
            >
              Reenviar código
            </button>

            {error && <p style={{ color: "red" }}>{error}</p>}
            {message && <p style={{ color: "green" }}>{message}</p>}
          </form>
        )}
      </div>
    </div>
  );
};

export default LoginForm;
