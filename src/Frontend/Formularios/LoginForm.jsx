import React from "react";
import './LoginForm.css';
import { FaUser, FaLock  } from "react-icons/fa";
import React from 'react';
import React from 'react';
import { Link } from 'react-router-dom';


const LoginForm = () => {
    return (
        <div className= 'wrapper'>
            <form action="">
                <h1>Login</h1>
                <div className="input-box">
                    <input type="text" placeholder='Nombre de Usuario' required /><FaUser className="icon"/>
                </div>
                <div className="input-box">
                    <input type="password" placeholder='Contraseña' required /><FaLock className="icon"/>
                </div>
                <div className="remember-forgot">
                    <label><input type="checkbox" />Recordar</label>
                    <a href="#">¿Olvidaste tu contraseña?</a>
                </div>

                <button type="submit">Ingresar</button>

                <div className="register-link">
                    <p>¿No tienes una cuenta? <link to="/Registrar">Registrate</link></p>
                </div>
            </form>
        </div>
    );
};

export default LoginForm;