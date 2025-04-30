import React, { useState, useEffect } from "react";
import { FaSave, FaEdit } from "react-icons/fa";
import { MdDelete, MdCancel } from "react-icons/md";
import Adminlte from "./adminlte";
import Swal from "sweetalert2";
import { Outlet } from "react-router-dom";
import "./GestionTelefono.css"; // Recuerda crear este CSS

const GestionTelefonos = () => {
  const [telefonos, setTelefonos] = useState([]);
  const [editingTelefonoId, setEditingTelefonoId] = useState(null);
  const [editedTelefonoData, setEditedTelefonoData] = useState({});
  const [textoFiltro, setTextoFiltro] = useState("");
  const [cantidad, setCantidad] = useState(3);
  const [paginaActual, setPaginaActual] = useState(1);

  useEffect(() => {
    fetchTelefonos();
  }, []);

  const fetchTelefonos = async () => {
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/telefonos/`);
      const data = await res.json();
      setTelefonos(data);
    } catch (error) {
      console.error("Error al cargar teléfonos:", error);
    }
  };

  const handleEditClick = (telefono) => {
    setEditingTelefonoId(telefono.cod_telefono);
    setEditedTelefonoData(telefono);
  };

  const handleSaveClick = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/telefonos/${editingTelefonoId}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(editedTelefonoData),
        }
      );

      if (!response.ok) throw new Error("Error al actualizar el teléfono.");

      await fetchTelefonos();
      setEditingTelefonoId(null);
      setEditedTelefonoData({});

      Swal.fire(
        "¡Actualizado!",
        "El teléfono ha sido actualizado correctamente.",
        "success"
      );
    } catch (error) {
      console.error(error);
      Swal.fire("Error", error.message, "error");
    }
  };

  const handleDelete = async (cod_telefono) => {
    const confirm = await Swal.fire({
      title: "¿Seguro que quieres eliminar este teléfono?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar",
    });

    if (confirm.isConfirmed) {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL}/telefonos/${cod_telefono}`,
          {
            method: "DELETE",
          }
        );

        if (!response.ok) throw new Error("Error al eliminar el teléfono.");

        await fetchTelefonos();

        Swal.fire("Eliminado", "Teléfono eliminado correctamente.", "success");
      } catch (error) {
        console.error(error);
        Swal.fire("Error", error.message, "error");
      }
    }
  };

  const telefonosFiltrados = telefonos.filter((telefono) =>
    telefono.telefono_principal?.toString().includes(textoFiltro)
  );

  const totalPaginas = Math.ceil(telefonosFiltrados.length / cantidad);

  return (
    <div>
      <Adminlte />
      <div className="content-wrapper">
        <h1> </h1>
        <section className="content">
          <div className="card-header">
            <div className="titulo-contenedor">
              <h3 className="card-title">GESTIÓN DE TELÉFONOS</h3>
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
                placeholder="Filtrar por número..."
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
                  <th>Teléfono Principal</th>
                  <th>Extensión</th>
                  <th>Código Área</th>
                  <th>Tipo Teléfono</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {telefonosFiltrados.length > 0 ? (
                  telefonosFiltrados
                    .slice(
                      (paginaActual - 1) * cantidad,
                      paginaActual * cantidad
                    )
                    .map((telefono) => (
                      <tr key={telefono.cod_telefono}>
                        <td>{telefono.cod_telefono}</td>
                        <td>{telefono.cod_persona}</td>
                        <td>
                          {editingTelefonoId === telefono.cod_telefono ? (
                            <input
                              type="text"
                              className="input-editar"
                              value={
                                editedTelefonoData.telefono_principal || ""
                              }
                              onChange={(e) =>
                                setEditedTelefonoData({
                                  ...editedTelefonoData,
                                  telefono_principal: e.target.value,
                                })
                              }
                            />
                          ) : (
                            telefono.telefono_principal
                          )}
                        </td>
                        <td>
                          {editingTelefonoId === telefono.cod_telefono ? (
                            <input
                              type="number"
                              className="input-editar"
                              value={editedTelefonoData.exten || ""}
                              onChange={(e) =>
                                setEditedTelefonoData({
                                  ...editedTelefonoData,
                                  exten: e.target.value,
                                })
                              }
                            />
                          ) : (
                            telefono.exten || "-"
                          )}
                        </td>
                        <td>
                          {editingTelefonoId === telefono.cod_telefono ? (
                            <input
                              type="number"
                              className="input-editar"
                              value={editedTelefonoData.codigo_area || ""}
                              onChange={(e) =>
                                setEditedTelefonoData({
                                  ...editedTelefonoData,
                                  codigo_area: e.target.value,
                                })
                              }
                            />
                          ) : (
                            telefono.codigo_area
                          )}
                        </td>
                        <td>
                          {editingTelefonoId === telefono.cod_telefono ? (
                            <input
                              type="number"
                              className="input-editar"
                              value={editedTelefonoData.cod_tipo_telefono || ""}
                              onChange={(e) =>
                                setEditedTelefonoData({
                                  ...editedTelefonoData,
                                  cod_tipo_telefono: e.target.value,
                                })
                              }
                            />
                          ) : (
                            telefono.cod_tipo_telefono
                          )}
                        </td>
                        <td>
                          {editingTelefonoId === telefono.cod_telefono ? (
                            <input
                              type="text"
                              className="input-editar"
                              value={editedTelefonoData.estado || ""}
                              onChange={(e) =>
                                setEditedTelefonoData({
                                  ...editedTelefonoData,
                                  estado: e.target.value,
                                })
                              }
                            />
                          ) : (
                            telefono.estado
                          )}
                        </td>
                        <td>
                          {editingTelefonoId === telefono.cod_telefono ? (
                            <>
                              <button
                                onClick={handleSaveClick}
                                className="new-telefono-save-btn"
                              >
                                <FaSave /> Guardar
                              </button>
                              <button
                                onClick={() => setEditingTelefonoId(null)}
                                className="new-telefono-cancel-btn"
                              >
                                <MdCancel /> Cancelar
                              </button>
                            </>
                          ) : (
                            <>
                              <button
                                className="new-telefono-edit-btn"
                                onClick={() => handleEditClick(telefono)}
                              >
                                <FaEdit /> Editar
                              </button>
                              <button
                                className="new-telefono-delete-btn"
                                onClick={() =>
                                  handleDelete(telefono.cod_telefono)
                                }
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
                    <td colSpan="8">No hay teléfonos disponibles.</td>
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
        <Outlet />
      </div>
    </div>
  );
};

export default GestionTelefonos;
