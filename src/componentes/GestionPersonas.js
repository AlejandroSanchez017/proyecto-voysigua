import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { FaSave, FaEdit } from "react-icons/fa";
import { MdDelete, MdCancel } from "react-icons/md";
import "./GestionPersonas.css";
import Swal from "sweetalert2";
import Adminlte from "./adminlte";
import { tienePermiso } from "../Utils/permisos";

const GestionPersonas = () => {
  const [textoFiltro, setTextoFiltro] = useState("");
  const [personas, setPersonas] = useState([]);
  const [error, setError] = useState(null);
  const location = useLocation();
  const [cantidad, setCantidad] = useState(3);
  const [editingPersonasId, setEditingPersonasId] = useState(null);
  const [editedPersonasData, setEditedPersonasData] = useState({});
  const [paginaActual, setPaginaActual] = useState(1);

  // Cargar script solo en esta página
  useEffect(() => {
    if (location.pathname === "/Gestion_Personas") {
      const script = document.createElement("script");
      script.src = "/plugins/sparklines/sparkline.js";
      script.async = true;
      document.body.appendChild(script);
      return () => {
        document.body.removeChild(script);
      };
    }
  }, [location]);

  // Cargar personas
  useEffect(() => {
    const fetchPersonas = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/personas`);
        const data = await response.json();
        setPersonas(data);
      } catch (error) {
        console.error("Error al cargar personas:", error);
        setError("Error al cargar personas");
      }
    };
    fetchPersonas();
  }, []);

  const handleEditClick = (persona) => {
    setEditingPersonasId(persona.cod_persona);
    setEditedPersonasData(persona);
  };

  const handleSaveClick = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/${editingPersonasId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(editedPersonasData),
        }
      );

      if (!response.ok) throw new Error("Error al actualizar la persona");

      const fetchUpdatedPersonas = async () => {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/personas`);
        const data = await response.json();
        setPersonas(data);
      };
      await fetchUpdatedPersonas();

      setEditingPersonasId(null);
      setEditedPersonasData({});
      Swal.fire(
        "¡Actualización exitosa!",
        "La persona ha sido actualizada.",
        "success"
      );
    } catch (error) {
      console.error("Error actualizando la persona:", error);
      Swal.fire("Error", "No se pudo actualizar la persona.", "error");
    }
  };

  const deletePersonasFromServer = async (cod_persona) => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/personas/${cod_persona}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        return { success: true };
      } else {
        const responseBody = await response.text();
        return {
          success: false,
          message: responseBody || "No se pudo eliminar la persona.",
        };
      }
    } catch (error) {
      console.error("Error al eliminar:", error);
      return { success: false, message: "Error al conectar con el servidor." };
    }
  };

  const handleDelete = async (cod_persona) => {
    const result = await Swal.fire({
      title: "¿Estás seguro?",
      text: "Esta acción no se puede deshacer.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar",
    });

    if (result.isConfirmed) {
      const response = await deletePersonasFromServer(cod_persona);
      if (response.success) {
        setPersonas((prev) =>
          prev.filter((p) => p.cod_persona !== cod_persona)
        );
        Swal.fire("¡Eliminado!", "La persona ha sido eliminada.", "success");
      } else {
        Swal.fire("Error", response.message, "error");
      }
    }
  };

  const personasFiltradas = personas.filter((persona) =>
    persona.primer_nombre.toLowerCase().includes(textoFiltro.toLowerCase())
  );

  const totalPaginas = Math.ceil(personasFiltradas.length / cantidad);

  return (
    <div>
      <Adminlte />
      <div className="content-wrapper">
        <section className="content">
          <div className="card-header">
            <div className="titulo-contenedor">
              <h3 className="card-title">MÓDULO DE PERSONAS</h3>
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
                  <option value="3">3</option>
                  <option value="10">10</option>
                  <option value="20">20</option>
                </select>
              </label>

              <input
                type="text"
                placeholder="Filtrar por Nombre..."
                value={textoFiltro}
                onChange={(e) => setTextoFiltro(e.target.value)}
                className="input-filtro"
              />
            </div>
          </div>

          {error && <p style={{ color: "red" }}>Error: {error}</p>}

          {/* Tabla */}
          <div className="card-body">
            <table className="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>Codigo de persona</th>
                  <th>Codigo Tipo Persona</th>
                  <th>Dni</th>
                  <th>Nombres</th>
                  <th>Apellidos</th>
                  <th>Fecha nacimiento</th>
                  <th>Sexo</th>
                  <th>Correo</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {personasFiltradas.length > 0 ? (
                  personasFiltradas
                    .slice(
                      (paginaActual - 1) * cantidad,
                      paginaActual * cantidad
                    )
                    .map((persona) => (
                      <tr key={persona.cod_persona}>
                        <td>{persona.cod_persona}</td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <input
                              className="input-editar"
                              type="number"
                              name="cod_tipo_persona"
                              value={editedPersonasData.cod_tipo_persona || ""}
                              onChange={(e) =>
                                setEditedPersonasData({
                                  ...editedPersonasData,
                                  cod_tipo_persona: e.target.value,
                                })
                              }
                            />
                          ) : (
                            persona.cod_tipo_persona
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <input
                              className="input-editar"
                              type="text"
                              name="dni"
                              value={editedPersonasData.dni || ""}
                              onChange={(e) =>
                                setEditedPersonasData({
                                  ...editedPersonasData,
                                  dni: e.target.value,
                                })
                              }
                            />
                          ) : (
                            persona.dni
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <input
                              className="input-editar"
                              type="text"
                              name="primer_nombre"
                              value={editedPersonasData.primer_nombre || ""}
                              onChange={(e) =>
                                setEditedPersonasData({
                                  ...editedPersonasData,
                                  primer_nombre: e.target.value,
                                })
                              }
                            />
                          ) : (
                            persona.primer_nombre
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <input
                              className="input-editar"
                              type="text"
                              name="apellido"
                              value={editedPersonasData.apellido || ""}
                              onChange={(e) =>
                                setEditedPersonasData({
                                  ...editedPersonasData,
                                  apellido: e.target.value,
                                })
                              }
                            />
                          ) : (
                            persona.apellido
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <input
                              className="input-editar"
                              type="date"
                              name="fecha_nacimiento"
                              value={editedPersonasData.fecha_nacimiento || ""}
                              onChange={(e) =>
                                setEditedPersonasData({
                                  ...editedPersonasData,
                                  fecha_nacimiento: e.target.value,
                                })
                              }
                            />
                          ) : (
                            persona.fecha_nacimiento
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <input
                              className="input-editar"
                              type="text"
                              name="sexo"
                              value={editedPersonasData.sexo || ""}
                              onChange={(e) =>
                                setEditedPersonasData({
                                  ...editedPersonasData,
                                  sexo: e.target.value,
                                })
                              }
                            />
                          ) : (
                            persona.sexo
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <input
                              className="input-editar"
                              type="text"
                              name="correo"
                              value={editedPersonasData.correo || ""}
                              onChange={(e) =>
                                setEditedPersonasData({
                                  ...editedPersonasData,
                                  correo: e.target.value,
                                })
                              }
                            />
                          ) : (
                            persona.correo
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <input
                              className="input-editar"
                              type="text"
                              name="estado"
                              value={editedPersonasData.estado || ""}
                              onChange={(e) =>
                                setEditedPersonasData({
                                  ...editedPersonasData,
                                  estado: e.target.value,
                                })
                              }
                            />
                          ) : (
                            persona.estado
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <>
                              {tienePermiso("actualizar_personas") && (
                                <button
                                  onClick={handleSaveClick}
                                  className="new-personas-save-btn"
                                >
                                  <FaSave /> Guardar
                                </button>
                              )}
                              <button
                                className="new-personas-cancel-btn"
                                onClick={() => setEditingPersonasId(null)}
                              >
                                <MdCancel /> Cancelar
                              </button>
                            </>
                          ) : (
                            <>
                              {tienePermiso("editar_personas") && (
                                <button
                                  className="new-personas-edit-btn"
                                  onClick={() => handleEditClick(persona)}
                                >
                                  <FaEdit /> Editar
                                </button>
                              )}
                              {tienePermiso("eliminar_personas") && (
                                <button
                                  className="new-personas-delete-btn"
                                  onClick={() =>
                                    handleDelete(persona.cod_persona)
                                  }
                                >
                                  <MdDelete /> Eliminar
                                </button>
                              )}
                            </>
                          )}
                        </td>
                      </tr>
                    ))
                ) : (
                  <tr>
                    <td colSpan="10">No hay personas disponibles.</td>
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

export default GestionPersonas;
