import React from "react";
import { Link } from "react-router-dom";

function Header() {
  const handleFullscreenToggle = () => {
    if (!document.fullscreenElement) {
      // Si no está en pantalla completa, ponerlo en pantalla completa
      document.documentElement.requestFullscreen().catch((err) => {
        console.error("Error al intentar activar la pantalla completa: ", err);
      });
    } else {
      // Si está en pantalla completa, salir de pantalla completa
      if (document.exitFullscreen) {
        document.exitFullscreen().catch((err) => {
          console.error("Error al intentar salir de pantalla completa: ", err);
        });
      }
    }
  };
  const handlePushMenuToggle = () => {
    // Aquí puedes manejar la lógica para abrir o cerrar el menú.
    console.log("El menú ha sido activado");
  };
  return (
    <div>
      {/* Navbar */}
      <nav className="main-header navbar navbar-expand navbar-white navbar-light">
        {/* Left navbar links */}
        <ul className="navbar-nav">
          <li className="nav-item">
            <button
              className="nav-link"
              data-widget="pushmenu"
              onClick={handlePushMenuToggle}
              aria-label="Abrir menú lateral"
              style={{
                background: "none", // Quita el fondo
                border: "none", // Quita el borde
                padding: 10, // Elimina el padding
                cursor: "pointer", // Cambia el cursor a mano cuando se pasa sobre el botón
              }}
            >
              <i className="fas fa-bars" />
            </button>
          </li>
          <li className="nav-item d-none d-sm-inline-block">
            <Link to="/home" className="nav-link active">
              <p>Home</p>
            </Link>
          </li>
        </ul>
        {/* Right navbar links */}
        <ul className="navbar-nav ml-auto">
          {/* Navbar Search */}
          <li className="nav-item">
            <div className="navbar-search-block">
              <form className="form-inline">
                <div className="input-group input-group-sm">
                  <input
                    className="form-control form-control-navbar"
                    type="search"
                    placeholder="Search"
                    aria-label="Search"
                  />
                  <div className="input-group-append">
                    <button className="btn btn-navbar" type="submit">
                      <i className="fas fa-search" />
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </li>
          <li className="nav-item">
            <button
              className="nav-link"
              onClick={handleFullscreenToggle}
              aria-label="Activar pantalla completa"
              style={{
                background: "none", // Quita el fondo
                border: "none", // Quita el borde
                padding: 10, // Elimina el padding
                cursor: "pointer", // Cambia el cursor a mano cuando se pasa sobre el botón
              }}
            >
              <i className="fas fa-expand-arrows-alt" />
            </button>
          </li>
        </ul>
      </nav>
      {/* /.navbar */}
    </div>
  );
}

export default Header;
