import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './LoginForm.css';
import { FaUser, FaLock } from "react-icons/fa";

const LoginForm = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const navigate = useNavigate();

    const handleLoginSubmit = async (e) => {
        e.preventDefault();

        // Credenciales de prueba 
        if (process.env.NODE_ENV === "development" && username === "admin" && password === "password123") {
            localStorage.setItem("authToken", "fakeDevToken");
            setErrorMessage("");
            console.log("Inicio de sesión de prueba exitoso");
            navigate("/home");
            return;
        }

        // Si no son las credenciales de prueba, procede con el flujo normal
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                throw new Error("Error en la autenticación");
            }

            const data = await response.json();
            const { token } = data;

            localStorage.setItem("authToken", token);
            console.log("Login exitoso, token almacenado:", token);
            setErrorMessage("");
            navigate("/home");
        } catch (error) {
            setErrorMessage("Error en la autenticación, revisa tus credenciales");
            console.error(error);
        }
    };

    return (
        <div className="wrapper">
            <form onSubmit={handleLoginSubmit}>
                <h1>Login</h1>
                <div className="input-box">
                    <input 
                        type="text" 
                        placeholder="Nombre de Usuario" 
                        value={username} 
                        onChange={(e) => setUsername(e.target.value)} 
                        required 
                    />
                    <FaUser className="icon" />
                </div>
                <div className="input-box">
                    <input 
                        type="password" 
                        placeholder="Contraseña" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                    />
                    <FaLock className="icon" />
                </div>
                {errorMessage && <p className="error">{errorMessage}</p>}
                <div className="remember-forgot">
                    <label><input type="checkbox" />Recordar</label>
                    <a href="#">¿Olvidaste tu contraseña?</a>
                </div>
                <button type="submit">Ingresar</button>
            </form>
        </div>
    );
};

export default LoginForm;