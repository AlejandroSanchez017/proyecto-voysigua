import React, { useState, useEffect } from "react";
import './LoginForm.css';
import { FaUser, FaLock  } from "react-icons/fa";



const LoginForm = () => {
    const [showModal, setShowModal] = useState(false);

    // Funciones para abrir y cerrar el modal
    const openModal = () => setShowModal(true);
    const closeModal = () => setShowModal(false);

    // Agregar o remover la clase 'modal-open' al body cuando se abre/cierra el modal
    useEffect(() => {
        if (showModal) {
            document.body.classList.add('modal-open');
        } else {
            document.body.classList.remove('modal-open');
        }
    }, [showModal]);

    return (
        <div>
            {!showModal && (
                <div className="wrapper">
                    <form action="">
                        <h1>Login</h1>
                        <div className="input-box">
                            <input type="text" placeholder="Nombre de Usuario" required />
                            <FaUser className="icon" />
                        </div>
                        <div className="input-box">
                            <input type="password" placeholder="Contraseña" required />
                            <FaLock className="icon" />
                        </div>
                        <div className="remember-forgot">
                            <label><input type="checkbox" />Recordar</label>
                            <a href="#">¿Olvidaste tu contraseña?</a>
                        </div>
                        <button type="submit">Ingresar</button>
                        <div className="register-link">
                            <a href="#" onClick={openModal}>¿No tienes una cuenta? Regístrate</a>
                        </div>
                    </form>
                </div>
            )}

            {showModal && (
                <div id="modal" className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={closeModal}>&times;</span>
                        <h2>Registro</h2>
                        <form>
                            <input type="text" placeholder="Nombre de Usuario" required />
                            <input type="email" placeholder="Correo Electrónico" required />
                            <input type="password" placeholder="Contraseña" required />
                            <input type="password" placeholder="Confirmar Contraseña" required />
                            <button type="submit">Registrar</button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default LoginForm;
