import React from "react";
import Adminlte from "./adminlte";
import "./HomePrincipal.css"; // Importa el CSS exclusivo


function HomePrincipal() {
  return (
    <div>
      <Adminlte />
      <div className="home2-container">
        {/* Contenido centrado */}
        <div className="home2-content">
          <h1 className="home2-title">
            Bienvenido al administrador de VoySigua
          </h1>
          <p className="home2-description">
            ¡Nosotros hacemos tus mandados! Solicita la diligencia que
            necesites, donde sea que estés, a la hora que tú lo requieras! Ahora
            contamos con envío de PAQUETERIA
          </p>

          {/* Información de contacto */}
          <div className="home2-contact-card">
            <h2>Contacto</h2>
            <p>
              <strong>📧 Correo:</strong> yovoysigua@gmail.com
            </p>
            <p>
              <strong>📱 Celular:</strong> ++04 9666-5019
            </p>
            <p>
              <strong>📍 Dirección:</strong> Siguatepeque 12111 Siguatepeque,
              Honduras
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePrincipal;
