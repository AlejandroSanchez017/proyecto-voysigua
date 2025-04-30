import React, { useState, useEffect } from "react";
import Swal from "sweetalert2";
import { FaEdit, FaSave } from "react-icons/fa";
import { MdDelete, MdCancel } from "react-icons/md";
import Adminlte from "./adminlte";
import "./GestionDirecciones.css";

const GestionDirecciones = () => {
  const [direcciones, setDirecciones] = useState([]);
  const [editingDireccionId, setEditingDireccionId] = useState(null);
  const [editedDireccionData, setEditedDireccionData] = useState({});
  const [textoFiltro, setTextoFiltro] = useState("");
  const [cantidad, setCantidad] = useState(10);
  const [paginaActual, setPaginaActual] = useState(1);

  useEffect(() => {
    fetchDirecciones();
  }, []);

  const fetchDirecciones = async () => {
    try {
      const response = await fetch("https://proyecto-backend.onrender.com/direcciones/");
      const data = await response.json();
      if (Array.isArray(data)) {
        setDirecciones(data);
      } else {
        setDirecciones([]);
      }
    } catch (error) {
      console.error("Error cargando direcciones:", error);
      setDirecciones([]);
    }
  };

  const handleEditClick = (direccion) => {
    setEditingDireccionId(direccion.cod_direccion);
    setEditedDireccionData(direccion);
  };

  const handleSaveClick = async () => {
    try {
      const response = await fetch(
        `https://proyecto-backend.onrender.com/direccion/${editingDireccionId}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(editedDireccionData),
        }
      );

      if (!response.ok) throw new Error("Error al actualizar dirección");

      await fetchDirecciones();
      setEditingDireccionId(null);
      setEditedDireccionData({});
      Swal.fire(
        "Actualizado",
        "La dirección ha sido actualizada correctamente",
        "success"
      );
    } catch (error) {
      console.error(error);
      Swal.fire("Error", "No se pudo actualizar la dirección", "error");
    }
  };

  const handleDelete = async (cod_direccion) => {
    const confirmacion = await Swal.fire({
      title: "¿Eliminar dirección?",
      text: "Esta acción no se puede deshacer",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar",
    });

    if (confirmacion.isConfirmed) {
      try {
        const response = await fetch(
          `https://proyecto-backend.onrender.com/direcciones/${cod_direccion}`,
          {
            method: "DELETE",
          }
        );

        if (!response.ok) throw new Error("Error al eliminar dirección");

        await fetchDirecciones();
        Swal.fire("Eliminado", "La dirección ha sido eliminada.", "success");
      } catch (error) {
        console.error(error);
        Swal.fire("Error", "No se pudo eliminar la dirección.", "error");
      }
    }
  };

  const direccionesFiltradas = Array.isArray(direcciones)
    ? direcciones.filter((dir) =>
        dir.cod_direccion.toString().includes(textoFiltro)
      )
    : [];

  const totalPaginas = Math.ceil(direccionesFiltradas.length / cantidad);
  return (
    <div>
      <Adminlte />
      <div className="content-wrapper">
        <h1> </h1>
        <section className="content">
          <div className="card-header">
            <div className="titulo-contenedor">
              <h3 className="card-title">GESTIÓN DE DIRECCIONES</h3>
            </div>
          </div>

          <div className="filtros-contenedor">
            <div className="grupo-filtros">
              <label className="label-mostrar">
                Mostrar&nbsp;
                <select
                  value={cantidad}
                  onChange={(e) => setCantidad(Number(e.target.value))}
                >
                  <option value="3">3</option>
                  <option value="10">10</option>
                  <option value="20">20</option>
                </select>
              </label>

              <input
                type="text"
                placeholder="Filtrar por Código..."
                value={textoFiltro}
                onChange={(e) => setTextoFiltro(e.target.value)}
                className="input-filtro"
              />
            </div>
          </div>

          <div className="card-body">
            <table className="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Persona</th>
                  <th>Ciudad</th>
                  <th>Tipo Dirección</th>
                  <th>Dirección 1</th>
                  <th>Dirección 2</th>
                  <th>Dirección 3</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {direccionesFiltradas.length > 0 ? (
                  direccionesFiltradas
                    .slice(
                      (paginaActual - 1) * cantidad,
                      paginaActual * cantidad
                    )
                    .map((direccion) => (
                      <tr key={direccion.cod_direccion}>
                        <td>{direccion.cod_direccion}</td>
                        <td>{direccion.cod_persona}</td>
                        <td>{direccion.cod_ciudad}</td>
                        <td>{direccion.cod_tipo_direccion}</td>
                        <td>
                          {editingDireccionId === direccion.cod_direccion ? (
                            <input
                              className="input-editar"
                              type="text"
                              value={editedDireccionData.direccion1 || ""}
                              onChange={(e) =>
                                setEditedDireccionData({
                                  ...editedDireccionData,
                                  direccion1: e.target.value,
                                })
                              }
                            />
                          ) : (
                            direccion.direccion1
                          )}
                        </td>
                        <td>
                          {editingDireccionId === direccion.cod_direccion ? (
                            <input
                              className="input-editar"
                              type="text"
                              value={editedDireccionData.direccion2 || ""}
                              onChange={(e) =>
                                setEditedDireccionData({
                                  ...editedDireccionData,
                                  direccion2: e.target.value,
                                })
                              }
                            />
                          ) : (
                            direccion.direccion2
                          )}
                        </td>
                        <td>
                          {editingDireccionId === direccion.cod_direccion ? (
                            <input
                              className="input-editar"
                              type="text"
                              value={editedDireccionData.direccion3 || ""}
                              onChange={(e) =>
                                setEditedDireccionData({
                                  ...editedDireccionData,
                                  direccion3: e.target.value,
                                })
                              }
                            />
                          ) : (
                            direccion.direccion3
                          )}
                        </td>
                        <td>
                          {editingDireccionId === direccion.cod_direccion ? (
                            <input
                              type="text"
                              className="input-editar"
                              value={editedDireccionData.estado_direccion || ""}
                              onChange={(e) =>
                                setEditedDireccionData({
                                  ...editedDireccionData,
                                  estado: e.target.value,
                                })
                              }
                            />
                          ) : (
                            direccion.estado_direccion
                          )}
                        </td>
                        <td>
                          {editingDireccionId === direccion.cod_direccion ? (
                            <>
                              <button
                                onClick={handleSaveClick}
                                className="new-direcciones-save-btn"
                              >
                                <FaSave /> Guardar
                              </button>
                              <button
                                onClick={() => setEditingDireccionId(null)}
                                className="new-direcciones-cancel-btn"
                              >
                                <MdCancel /> Cancelar
                              </button>
                            </>
                          ) : (
                            <>
                              <button
                                onClick={() => handleEditClick(direccion)}
                                className="new-direcciones-edit-btn"
                              >
                                <FaEdit /> Editar
                              </button>
                              <button
                                onClick={() =>
                                  handleDelete(direccion.cod_direccion)
                                }
                                className="new-direcciones-delete-btn"
                              >
                                <MdDelete /> Eliminar
                              </button>
                            </>
                          )}
                        </td>
                      </tr>
                    ))
                ) : (
                  <tr>
                    <td colSpan="9">No hay direcciones disponibles.</td>
                  </tr>
                )}
              </tbody>
            </table>
            <div className="paginacion">
              <button
                onClick={() => setPaginaActual(1)}
                disabled={paginaActual === 1}
              >
                {"<<"}
              </button>
              <button
                onClick={() => setPaginaActual(paginaActual - 1)}
                disabled={paginaActual === 1}
              >
                {"<"}
              </button>
              <span>
                Página {paginaActual} de {totalPaginas}
              </span>
              <button
                onClick={() => setPaginaActual(paginaActual + 1)}
                disabled={paginaActual === totalPaginas}
              >
                {">"}
              </button>
              <button
                onClick={() => setPaginaActual(totalPaginas)}
                disabled={paginaActual === totalPaginas}
              >
                {">>"}
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default GestionDirecciones;
