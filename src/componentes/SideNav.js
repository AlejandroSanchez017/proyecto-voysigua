import React from "react";
import { Link } from "react-router-dom";

function App() {
  return (
    <div className="">
      
      {/* Main Sidebar Container */}
      <aside className="main-sidebar sidebar-dark-primary elevation-4">
        {/* Brand Logo */}
        <a href="index.html" className="brand-link">
          <img
            src="dist/img/logo.png"
            alt="AdminLTE Logo"
            className="brand-image img-circle elevation-3"
            style={{ opacity: ".8" }}
          />
          <span className="brand-text font-weight-light">VoySigua</span>
        </a>
        {/* Sidebar */}
        <div className="sidebar">
          {/* Sidebar user panel (optional) */}
          <div className="user-panel mt-3 pb-3 mb-3 d-flex">
            <div className="image">
              <img
                src="dist/img/logo.png"
                className="img-circle elevation-2"
                alt="logo"
              />
            </div>
            <div className="info">
              <a href="./LoginForm.js" className="d-block">
                Iniciar Sesion
              </a>
            </div>
          </div>
          {/* SidebarSearch Form */}
          <div className="form-inline">
            <div className="input-group" data-widget="sidebar-search">
              <input
                className="form-control form-control-sidebar"
                type="search"
                placeholder="Search"
                aria-label="Search"
              />
              <div className="input-group-append">
                <button className="btn btn-sidebar">
                  <i className="fas fa-search fa-fw" />
                </button>
              </div>
            </div>
          </div>
          {/* Sidebar Menu */}
          <nav className="mt-2">
            <ul
              className="nav nav-pills nav-sidebar flex-column"
              data-widget="treeview"
              role="menu"
              data-accordion="false"
            >
              {/* Add icons to the links using the .nav-icon class
         with font-awesome or any other icon font library */}
              <li className="nav-item menu-open">
                <a href="#" className="nav-link active">
                  <i className="nav-icon fas fa-tachometer-alt" />
                  <p>
                    Gestion
                    <i className="right fas fa-angle-left" />
                  </p>
                </a>
                <ul className="nav nav-treeview">
                  <li className="nav-item">
                    <Link to="/mycomponent" className="nav-link active">
                      <i className="far fa-circle nav-icon" />
                      <p>Gestion Usuario</p>
                    </Link>
                  </li>
                  <li className="nav-item">
                  <Link to="/gestionpersonas" className="nav-link active">
                      <i className="far fa-circle nav-icon" />
                      <p>Gestion Personas</p>
                    </Link>
                  </li>
                  <li className="nav-item">
                  <Link to="/gestionempleados" className="nav-link active">
                      <i className="far fa-circle nav-icon" />
                      <p>Gestion Empleados</p>
                    </Link>
                  </li>
                </ul>
              </li>
              {/*MODULOS ADMINISTATIVOS*/}
              <li className="nav-item menu-open">
                <a href="#" className="nav-link active">
                  <i className="nav-icon fas fa-tachometer-alt" />
                  <p>
                    Modulos
                    <i className="right fas fa-angle-left" />
                  </p>
                </a>
                <ul className="nav nav-treeview">
                  <li className="nav-item">
                    <a href="./index.html" className="nav-link active">
                      <i className="far fa-circle nav-icon" />
                      <p>Modulo Paqueteria</p>
                    </a>
                  </li>
                  <li className="nav-item">
                    <a href="./index.html" className="nav-link">
                      <i className="far fa-circle nav-icon" />
                      <p>Modulo Mandados</p>
                    </a>
                  </li>
                  <li className="nav-item">
                    <a href="./index.html" className="nav-link">
                      <i className="far fa-circle nav-icon" />
                      <p>Modulo administracion</p>
                    </a>
                  </li>
                </ul>
              </li>
            </ul>
          </nav>
          {/* /.sidebar-menu */}
        </div>
        {/* /.sidebar  */}
      </aside>
    </div>
  );
}

export default App;
