import React, { useState } from "react";
import { Link } from "react-router-dom";
import { tienePermiso } from "../Utils/permisos";
import {
  FaUserPlus,
  FaSearch,
  FaShoppingCart,
  FaBoxOpen,
} from "react-icons/fa";
import { BsTools } from "react-icons/bs";
import { IoIosArrowDown, IoIosArrowUp } from "react-icons/io";
import "./SideNav.css";

function SideNav({ setIsAuthenticated }) {
  const username = sessionStorage.getItem("username") || "Iniciar Sesión";
  const [searchTerm, setSearchTerm] = useState("");
  const [openSection, setOpenSection] = useState(null);

  const toggleAccordion = (section) => {
    setOpenSection(openSection === section ? null : section);
  };

  const handleLogout = () => {
    sessionStorage.removeItem("username");
    sessionStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <aside className="main-sidebar sidebar-dark-primary elevation-4 d-flex flex-column">
      <Link to="/" className="brand-link">
        <img
          src="dist/img/logo.png"
          alt="VoySigua"
          className="brand-image img-circle elevation-3"
          style={{ opacity: ".8" }}
        />
        <span className="brand-text font-weight-light">VoySigua</span>
      </Link>

      <div className="sidebar flex-grow-1">
        {/* Usuario */}
        <div className="user-panel mt-3 pb-3 mb-3 d-flex align-items-center">
          <div className="image">
            <img
              src="dist/img/logo.png"
              className="img-circle elevation-2"
              alt="User profile"
            />
          </div>
          <div className="info d-flex flex-column">
            <span className="text-white">{username}</span>
          </div>
        </div>

        {/* Buscador */}
        <div className="form-inline px-2 mb-2">
          <input
            className="form-control form-control-sidebar"
            type="search"
            placeholder="Buscar..."
            aria-label="Buscar"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {/* Navegación tipo acordeón */}
        <nav className="mt-2">
          <ul className="nav nav-pills nav-sidebar flex-column" role="menu">

            {/* MANDADOS */}
            <li className="nav-item">
              <div className="nav-link accordion-header" onClick={() => toggleAccordion("mandados")}>
                <p className="mb-0">Mandados</p>
                {openSection === "mandados" ? <IoIosArrowUp /> : <IoIosArrowDown />}
              </div>
              {openSection === "mandados" && (
                <ul className="nav-treeview">
                  <li className="nav-item">
                    <Link to="/nuevomandados" className="nav-link">
                      <FaUserPlus className="nav-icon" />
                      <p>Nuevo Mandado</p>
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/mandados" className="nav-link">
                      <FaShoppingCart className="nav-icon" />
                      <p>Consultar Mandado</p>
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/reportemandados" className="nav-link">
                      <FaShoppingCart className="nav-icon" />
                      <p>Reporte Mandado</p>
                    </Link>
                  </li>
                </ul>
              )}
            </li>

            {/* PAQUETES */}
            <li className="nav-item">
              <div className="nav-link accordion-header" onClick={() => toggleAccordion("paquetes")}>
                <p className="mb-0">Paquetes</p>
                {openSection === "paquetes" ? <IoIosArrowUp /> : <IoIosArrowDown />}
              </div>
              {openSection === "paquetes" && (
                <ul className="nav-treeview">
                  <li className="nav-item">
                    <Link to="/nuevopaquete" className="nav-link">
                      <FaUserPlus className="nav-icon" />
                      <p>Nuevo paquete</p>
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/estadopaquete" className="nav-link">
                      <FaBoxOpen className="nav-icon" />
                      <p>Estado Paquete</p>
                    </Link>
                  </li>
                </ul>
              )}
            </li>

            {/* ADMINISTRACIÓN */}
            <li className="nav-item">
              <div className="nav-link accordion-header" onClick={() => toggleAccordion("admin")}>
                <p className="mb-0">Administración</p>
                {openSection === "admin" ? <IoIosArrowUp /> : <IoIosArrowDown />}
              </div>
              {openSection === "admin" && (
                <ul className="nav-treeview">
                  <li className="nav-item">
                    <Link to="/modulo-admin" className="nav-link">
                      <FaSearch className="nav-icon" />
                      <p>Módulo Administración</p>
                    </Link>
                  </li>
                </ul>
              )}
            </li>
              
            {/* Modulo de seguridad */}
            <li className="nav-item">
              <div className="nav-link accordion-header" onClick={() => toggleAccordion("modulodeseguridad")}>
                <p className="mb-0">Modulo de Seguridad</p>
                {openSection === "modulodeseguridad" ? <IoIosArrowUp /> : <IoIosArrowDown />}
              </div>
              {openSection === "modulodeseguridad" && (
                <ul className="nav-treeview">
                  {tienePermiso("agregar_usuarios") && (
                    <li className="nav-item">
                      <Link to="/nuevousuario" className="nav-link">
                      <FaUserPlus className="nav-icon" />
                        <p>Nuevo Usuario</p>
                      </Link>
                    </li>
                  )}
                  {tienePermiso("consultar_usuarios") && (
                    <li className="nav-item">
                      <Link to="/mycomponent" className="nav-link">
                      <BsTools className="nav-icon"/>
                        <p>Modulo Usuario</p>
                      </Link>
                    </li>
                  )}
                </ul>
              )}
            </li>

            {/* Modulo de personas*/}
            <li className="nav-item">
              <div className="nav-link accordion-header" onClick={() => toggleAccordion("gestiones")}>
                <p className="mb-0">Modulo de Personas</p>
                {openSection === "gestiones" ? <IoIosArrowUp /> : <IoIosArrowDown />}
              </div>
              {openSection === "gestiones" && (
                <ul className="nav-treeview">
                  {tienePermiso("agregar_personas") && (
                    <li className="nav-item">
                      <Link to="/nuevapersona" className="nav-link">
                      <FaUserPlus className="nav-icon" />
                        <p>Nueva Persona</p>
                      </Link>
                    </li>
                  )}
                  {tienePermiso("agregar_empleados") && (
                    <li className="nav-item">
                      <Link to="/nuevoempleado" className="nav-link">
                      <FaUserPlus className="nav-icon" />
                        <p>Nuevo Empleado</p>
                      </Link>
                    </li>
                  )}
                  {tienePermiso("consultar_personas") && (
                    <li className="nav-item">
                      <Link to="/gestionpersonas" className="nav-link">
                      <BsTools className="nav-icon"/>
                        <p>Modulo de Personas</p>
                      </Link>
                    </li>
                  )}
                  {tienePermiso("consultar_empleados") && (
                    <li className="nav-item">
                      <Link to="/gestionempleados" className="nav-link">
                      <BsTools className="nav-icon"/>
                        <p>Modulo de Empleados</p>
                      </Link>
                    </li>
                  )}
                  {tienePermiso("consultar_personas") && (
                    <li className="nav-item">
                      <Link to="/gestiontelefonos" className="nav-link">
                      <BsTools className="nav-icon"/>
                        <p>Modulo de telefonos</p>
                      </Link>
                    </li>
                  )}
                  {tienePermiso("consultar_personas") && (
                    <li className="nav-item">
                      <Link to="/gestiondirecciones" className="nav-link">
                      <BsTools className="nav-icon"/>
                        <p>Modulo de Direcciones</p>
                      </Link>
                    </li>
                  )}
                </ul>
              )}
            </li>
            <li className="nav-item">
              <div className="nav-link accordion-header" onClick={() => toggleAccordion("auditoria")}>
                <p className="mb-0">Auditoria</p>
                {openSection === "auditoria" ? <IoIosArrowUp /> : <IoIosArrowDown />}
              </div>
              {openSection === "auditoria" && (
                <ul className="nav-treeview">
                  <li className="nav-item">
                    <Link to="/auditoria" className="nav-link">
                      <BsTools className="nav-icon"/>
                      <p>Auditoria</p>
                    </Link>
                  </li>
                </ul>
              )}
            </li>
          </ul>
        </nav>
      </div>

      {/* Cierre de sesión */}
      {username !== "Iniciar Sesión" && (
        <div className="p-3 border-top">
          <button
            onClick={handleLogout}
            className="btn btn-outline-light btn-block"
          >
            Cerrar sesión
          </button>
        </div>
      )}
    </aside>
  );
}

export default SideNav;

