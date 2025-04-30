import React, { useState, useEffect } from "react";
import Adminlte from "./adminlte";
import "./Auditoria.css";

const Auditoria = () => {
  const [auditoria, setAuditoria] = useState([]);
  const [error, setError] = useState("");
  const [cantidad, setCantidad] = useState(10);
  const [textoFiltro, setTextoFiltro] = useState("");
  const [paginaActual, setPaginaActual] = useState(1);


  useEffect(() => {
    const fetchAuditoria = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/auditoria/`);
        const data = await response.json();
        if (Array.isArray(data)) {
          setAuditoria(data);
        } else {
          setAuditoria([]);
        }
      } catch (err) {
        console.error("Error al cargar auditoría:", err);
        setError("No se pudo cargar la auditoría");
      }
    };

    fetchAuditoria();
  }, []);

  

  const auditoriaFiltrada = auditoria.filter((registro) => {
    const texto = textoFiltro.toLowerCase();
    return (
      registro.tabla?.toLowerCase().includes(texto) ||
      registro.campo?.toLowerCase().includes(texto) ||
      registro.usuario?.toLowerCase().includes(texto)
    );
  });

  const totalPaginas = Math.ceil(auditoriaFiltrada.length / cantidad);


  return (
    <div>
      <Adminlte />
      <div className="content-wrapper">
        <section className="content">
          <div className="card-header">
            <div className="titulo-contenedor">
              <h3 className="card-title">MÓDULO DE AUDITORÍA</h3>
            </div>
          </div>

          {/* Filtros */}
          <div className="filtros-contenedor">
            <div className="grupo-filtros">
              <label className="label-mostrar">
                Mostrar&nbsp;
                <select
  value={cantidad}
  onChange={(e) => setCantidad(Number(e.target.value))}
>
  <option value="10">10</option>
  <option value="20">20</option>
  <option value="50">50</option>
  <option value="-1">Todos</option> {/* 🔥 Esta opción nueva */}
</select>
              </label>
              <input
                type="text"
                placeholder="Filtrar por Tabla, Campo o Usuario..."
                value={textoFiltro}
                onChange={(e) => setTextoFiltro(e.target.value)}
                className="input-filtro"
              />
            </div>
          </div>

          {error && <p style={{ color: "red" }}>{error}</p>}

          {/* Tabla */}
          <div className="card-body">
            <table className="table table-auditoria">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Tipo</th>
                  <th>Tabla</th>
                  <th>Registro</th>
                  <th>Campo</th>
                  <th>Valor Antes</th>
                  <th>Valor Después</th>
                  <th>Fecha</th>
                  <th>Usuario</th>
                  <th>PC</th>
                </tr>
              </thead>
              <tbody>
              {auditoriaFiltrada.length > 0 ? (
  auditoriaFiltrada
    .slice((paginaActual - 1) * cantidad, paginaActual * cantidad)
    .map((registro) => (
      <tr key={registro.idauditoria}>
        <td>{registro.idauditoria}</td>
        <td>{registro.tipo}</td>
        <td>{registro.tabla}</td>
        <td>{registro.registro}</td>
        <td>{registro.campo}</td>
        <td>{registro.valorantes || "-"}</td>
        <td>{registro.valordespues || "-"}</td>
        <td>{registro.fecha}</td>
        <td>{registro.usuario}</td>
        <td>{registro.pc}</td>
      </tr>
    ))
) : (
  <tr>
    <td colSpan="10">No hay registros de auditoría disponibles.</td>
  </tr>
)}
              </tbody>
            </table>
            <div className="paginacion">
  <button onClick={() => setPaginaActual(1)} disabled={paginaActual === 1}>
    {"<<"}
  </button>
  <button onClick={() => setPaginaActual(paginaActual - 1)} disabled={paginaActual === 1}>
    {"<"}
  </button>
  <span>Página {paginaActual} de {totalPaginas}</span>
  <button onClick={() => setPaginaActual(paginaActual + 1)} disabled={paginaActual === totalPaginas}>
    {">"}
  </button>
  <button onClick={() => setPaginaActual(totalPaginas)} disabled={paginaActual === totalPaginas}>
    {">>"}
  </button>
</div>

          </div>
        </section>
      </div>
    </div>
  );
};

export default Auditoria;
