import React from "react";
import Adminlte from "./adminlte";
import "./HomePrincipal.css"; // Asegúrate de tener el archivo de estilos

function HomePrincipal() {
  return (
    <div>
      <Adminlte />
      <div className="home2-container">
        <div className="home2-content">
          <h1 className="home2-title">
            ¡Nosotros hacemos tus mandados!
          </h1>

          <p className="home2-description">
            En <strong>VoySigua</strong> nos dedicamos a brindar un servicio confiable, rápido y personalizado en mandados y paquetería dentro de Siguatepeque, Honduras.
            Te ayudamos a realizar diligencias sin que tengas que moverte de casa, ¡con atención inmediata desde redes o WhatsApp!
          </p>

          <p className="home2-description">
            Desde filas, compras, trámites hasta el envío de paquetes urgentes,
            nuestro equipo está listo para apoyarte con eficiencia y seguridad.
          </p>

          <div className="home2-contact-card">
            <h2>¿Por qué elegir VoySigua?</h2>
            <ul>
              <li>Rapidez y confianza</li>
              <li>Atención personalizada</li>
              <li>Tarifas accesibles</li>
              <li>Servicio 100% en línea</li>
            </ul>
          </div>

          <div className="home2-contact-card">
            <h2>Contacto</h2>
            <p>
              <strong> Correo:</strong> yovoysigua@gmail.com
            </p>
            <p>
              <strong> Celular / WhatsApp:</strong> +504 9666-5019
            </p>
            <p>
              <strong> Dirección:</strong> Siguatepeque 12111, Honduras
            </p>
            <p>
              <strong> Instagram:</strong>{" "}
              <a
                href="https://www.instagram.com/voy.hn/"
                target="_blank"
                rel="noopener noreferrer"
              >
                @voy.hn
              </a>
            </p>
            <p>
              <strong> Facebook:</strong>{" "}
              <a
                href="https://www.facebook.com/VoySiguatepeque"
                target="_blank"
                rel="noopener noreferrer"
              >
                Voy Siguatepeque
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePrincipal;
