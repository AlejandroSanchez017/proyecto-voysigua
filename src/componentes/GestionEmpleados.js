import React, { useState, useEffect } from "react";
import { Outlet } from "react-router-dom"; 
import { useLocation } from "react-router-dom";
import { FaSave, FaEdit } from "react-icons/fa";
import { MdDelete, MdCancel } from "react-icons/md";
import "./GestionEmpleados.css";
import Swal from "sweetalert2";
import Adminlte from "./adminlte";
import { tienePermiso } from "../Utils/permisos"; 

const GestionEmpleados = () => {
  const [textoFiltro, setTextoFiltro] = useState("");
  const [empleados, setEmpleados] = useState([]);
  const [error] = useState("");
  const location = useLocation();
  const [cantidad, setCantidad] = useState(3);
  const [editingEmpleadosId, setEditingEmpleadosId] = useState(null);
  const [editedEmpleadosData, setEditedEmpleadosData] = useState({});
  const [showNewEmpleadosRow, setShowNewEmpleadosRow] = useState(false);
  const [newEmpleadosData, setNewEmpleadosData] = useState({
    cod_persona: "",
    cod_tipo_empleado: "",
    cod_area: "",
    cod_tipo_contrato: "",
    fecha_salida: null,
    motivo_salida: null,
    fecha_contratacion: "",
    salario: "",
    estado_empleado: "",
  });

  useEffect(() => {
    if (location.pathname === "/Gestion_Empleados") {
      const script = document.createElement("script");
      script.src = "/plugins/sparklines/sparkline.js";
      script.async = true;
      document.body.appendChild(script);
      return () => {
        document.body.removeChild(script);
      };
    }
  }, [location]);

  useEffect(() => {
    const fetchEmpleados = async () => {
      try {
        const res = await fetch("http://localhost:8000/empleados/");
        const data = await res.json();
        if (Array.isArray(data)) {
          setEmpleados(data);
        } else {
          console.error(" Respuesta inesperada:", data);
          setEmpleados([]);
        }
      } catch (err) {
        console.error(" Error al cargar empleados:", err);
        setEmpleados([]);
      }
    };
    fetchEmpleados();
  }, []);

  const handleEditClick = (empleado) => {
    setEditingEmpleadosId(empleado.cod_empleado);
    setEditedEmpleadosData(empleado);
  };

  const handleSaveClick = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/empleados/${editingEmpleadosId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(editedEmpleadosData),
        }
      );

      if (!response.ok) throw new Error("Error al actualizar el Empleado");

      const updatedEmpleados = await fetch("http://localhost:8000/empleados");
      const data = await updatedEmpleados.json();
      setEmpleados(data);
      setEditingEmpleadosId(null);
      setEditedEmpleadosData({});

      Swal.fire({
        title: "¡Actualización exitosa!",
        text: "El Empleado ha sido actualizado correctamente.",
        icon: "success",
        confirmButtonText: "OK",
      });
    } catch (error) {
      console.error("Error actualizando el empleado:", error);
      Swal.fire({
        title: "Error",
        text: "No se pudo actualizar el empleado. Inténtalo de nuevo.",
        icon: "error",
        confirmButtonText: "OK",
      });
    }
  };

  const deleteEmpleadosFromServer = async (cod_empleado) => {
    try {
      const response = await fetch(
        `http://localhost:8000/empleados/${cod_empleado}`,
        {
          method: "DELETE",
        }
      );
      const responseBody = await response.text();

      if (response.ok) {
        return { success: true };
      } else {
        return {
          success: false,
          message: responseBody || "No se pudo eliminar el empleado.",
        };
      }
    } catch (error) {
      console.error("Error en la solicitud de eliminación:", error);
      return { success: false, message: "Error al conectar con el servidor." };
    }
  };

  const handleDelete = async (cod_empleado) => {
    const result = await Swal.fire({
      title: "¿Estás seguro?",
      text: "Esta acción no se puede deshacer. ¿Deseas eliminar al empleado?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar",
    });

    if (result.isConfirmed) {
      try {
        const response = await deleteEmpleadosFromServer(cod_empleado);

        if (response.success) {
          setEmpleados((prev) =>
            prev.filter((e) => e.cod_empleado !== cod_empleado)
          );
          Swal.fire({
            icon: "success",
            title: "Empleado eliminado",
            text: "El Empleado ha sido eliminado exitosamente.",
          });
        } else {
          throw new Error(response.message || "Error al eliminar el empleado.");
        }
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Error",
          text: error.message || "No se pudo eliminar el empleado.",
        });
        console.error("Error eliminando el empleado:", error);
      }
    }
  };

  const handleSaveNewEmpleados = async () => {
    try {
      const response = await fetch("http://localhost:8000/empleados/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newEmpleadosData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error al guardar:", errorData);
        throw new Error("Error al guardar el empleado en la base de datos");
      }

      const result = await response.json(); // El objeto completo con cod_empleado generado
      console.log("Empleado creado:", result);

      setEmpleados((prev) => [...prev, result]);

      setNewEmpleadosData({
        cod_persona: "",
        cod_tipo_empleado: "",
        cod_area: "",
        cod_tipo_contrato: "",
        fecha_salida: null,
        motivo_salida: null,
        fecha_contratacion: "",
        salario: "",
        estado_empleado: "",
      });
      setShowNewEmpleadosRow(false);

      Swal.fire({
        icon: "success",
        title: "Empleado guardado",
        text: "El empleado se ha guardado exitosamente.",
        confirmButtonColor: "#3085d6",
        confirmButtonText: "OK",
      });
    } catch (error) {
      console.error("Error:", error);
      Swal.fire({
        icon: "error",
        title: "Error al guardar el empleado",
        text: error.message,
        confirmButtonColor: "#d33",
        confirmButtonText: "OK",
      });
    }
  };

  const handleDespedirEmpleado = async (empleado) => {
    const { value: formValues } = await Swal.fire({
      title: `Despedir empleado ${empleado.cod_empleado}`,
      html:
        '<input id="fecha_salida" type="date" class="swal2-input" placeholder="Fecha de salida">' +
        '<input id="motivo_salida" class="swal2-input" placeholder="Motivo de salida">',
      focusConfirm: false,
      showCancelButton: true,
      confirmButtonText: "Despedir",
      preConfirm: () => {
        return {
          fecha_salida: document.getElementById("fecha_salida").value,
          motivo_salida: document.getElementById("motivo_salida").value,
        };
      },
    });
  
    if (formValues) {
      try {
        const response = await fetch(
          `http://localhost:8000/empleados/despedir/${empleado.cod_empleado}`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formValues),
          }
        );
  
        const result = await response.json();
  
        if (response.ok) {
          Swal.fire("Éxito", result.message, "success");
  
          // Recarga la lista de empleados
          const res = await fetch("http://localhost:8000/empleados/");
          const data = await res.json();
          setEmpleados(data);
        } else {
          throw new Error(result.detail || "Error al despedir al empleado.");
        }
      } catch (error) {
        console.error("Error al despedir:", error);
        Swal.fire("Error", error.message, "error");
      }
    }
  };
  

  const empleadosFiltrados = Array.isArray(empleados)
    ? empleados.filter((empleado) => {
        const cod = empleado?.cod_empleado?.toString() || "";
        return cod.includes(textoFiltro);
      })
    : [];

  return (
    <div>
      <Adminlte />
      <div className="content-wrapper">
        <h1> </h1>
        <section className="content">
          <div className="card-header">
            <div className="titulo-contenedor">
              <h3 className="card-title">MODULO DE EMPLEADOS</h3>
            </div>
          </div>
            <h1> </h1>
            {/* FILTROS DEBAJO DEL TÍTULO */}
            <div className="filtros-contenedor">
              <button
                onClick={() => setShowNewEmpleadosRow(true)}
                className="agregar-persona-btn"
              >
                AGREGAR Empleado
              </button>

              <div className="grupo-filtros">
                <label className="label-mostrar">
                  Mostrar&nbsp;
                  <select
                    value={cantidad}
                    onChange={(e) => setCantidad(Number(e.target.value))}
                  >
                    <option value="3">3</option>
                    <option value="10">10</option>
                    <option value="50">50</option>
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
          <div className="card-body">
            <table className="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>Codigo de Empleado</th>
                  <th>Persona</th>
                  <th>Tipo empleado</th>
                  <th>Area De Trabajo</th>
                  <th>Tipo Contrato</th>
                  <th>Fecha Salida</th>
                  <th>Motivo Salida</th>
                  <th>Fecha Contratacion</th>
                  <th>Salario</th>
                  <th>Estado Empleado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {showNewEmpleadosRow && (
                  <tr className="new-empleados-row">
                    <td className="new-empleados-cell">Nuevo Empleado</td>
                    <td className="new-empleados-cell">
                      <input
                        type="number"
                        className="new-empleados-input"
                        value={newEmpleadosData.cod_persona}
                        onChange={(e) =>
                          setNewEmpleadosData({
                            ...newEmpleadosData,
                            cod_persona: e.target.value,
                          })
                        }
                      />
                    </td>
                    <td className="new-empleados-cell">
                      <input
                        type="number"
                        className="new-empleados-input"
                        value={newEmpleadosData.cod_tipo_empleado}
                        onChange={(e) =>
                          setNewEmpleadosData({
                            ...newEmpleadosData,
                            cod_tipo_empleado: e.target.value,
                          })
                        }
                      />
                    </td>
                    <td className="new-empleados-cell">
                      <input
                        type="number"
                        className="new-empleados-input"
                        value={newEmpleadosData.cod_area}
                        onChange={(e) =>
                          setNewEmpleadosData({
                            ...newEmpleadosData,
                            cod_area: e.target.value,
                          })
                        }
                      />
                    </td>
                    <td className="new-empleados-cell">
                      <input
                        type="number"
                        className="new-empleados-input"
                        value={newEmpleadosData.cod_tipo_contrato}
                        onChange={(e) =>
                          setNewEmpleadosData({
                            ...newEmpleadosData,
                            cod_tipo_contrato: e.target.value,
                          })
                        }
                      />
                    </td>
                    <td fecha_salida> </td>
                    <td motivo_salida></td>
                    <td className="new-empleados-cell">
                      <input
                        type="date"
                        className="new-empleados-input"
                        value={newEmpleadosData.fecha_contratacion}
                        onChange={(e) =>
                          setNewEmpleadosData({
                            ...newEmpleadosData,
                            fecha_contratacion: e.target.value,
                          })
                        }
                      />
                    </td>
                    <td className="new-empleados-cell">
                      <input
                        type="number"
                        className="new-empleados-input"
                        value={newEmpleadosData.salario}
                        onChange={(e) =>
                          setNewEmpleadosData({
                            ...newEmpleadosData,
                            salario: e.target.value,
                          })
                        }
                      />
                    </td>
                    <td className="new-empleados-cell">
                      <input
                        type="text"
                        className="new-empleados-input"
                        value={newEmpleadosData.estado_empleado}
                        onChange={(e) =>
                          setNewEmpleadosData({
                            ...newEmpleadosData,
                            estado_empleado: e.target.value,
                          })
                        }
                      />
                    </td>
                    <td className="new-empleados-cell">
                      {tienePermiso("actualizar_empleados") && (
                        <button
                          onClick={handleSaveNewEmpleados}
                          className="new-empleados-save-btn"
                        >
                          <FaSave />
                          Guardar
                        </button>
                      )}
                      <button
                        onClick={() => setShowNewEmpleadosRow(false)}
                        className="new-empleados-cancel-btn"
                      >
                        <MdCancel />
                        Cancelar
                      </button>
                    </td>
                  </tr>
                )}
                {empleadosFiltrados.length > 0 ? (
                  empleadosFiltrados.map((empleado) => (
                    <tr key={empleado.cod_empleado}>
                      <td>{empleado.cod_empleado}</td>
                      <td>
                        {editingEmpleadosId === empleado.cod_empleado ? (
                          <input
                            className="input-editar"
                            type="number"
                            name="cod_persona"
                            value={editedEmpleadosData.cod_persona || ""}
                            onChange={(e) =>
                              setEditedEmpleadosData({
                                ...editedEmpleadosData,
                                cod_persona: e.target.value,
                              })
                            }
                          />
                        ) : (
                          empleado.cod_persona
                        )}
                      </td>
                      <td>
                        {editingEmpleadosId === empleado.cod_empleado ? (
                          <input
                            className="input-editar"
                            type="text"
                            name="cod_tipo_empleado"
                            value={editedEmpleadosData.cod_tipo_empleado || ""}
                            onChange={(e) =>
                              setEditedEmpleadosData({
                                ...editedEmpleadosData,
                                cod_tipo_empleado: e.target.value,
                              })
                            }
                          />
                        ) : (
                          empleado.cod_tipo_empleado
                        )}
                      </td>
                      <td>
                        {editingEmpleadosId === empleado.cod_empleado ? (
                          <input
                            className="input-editar"
                            type="text"
                            name="cod_area"
                            value={editedEmpleadosData.cod_area || ""}
                            onChange={(e) =>
                              setEditedEmpleadosData({
                                ...editedEmpleadosData,
                                cod_area: e.target.value,
                              })
                            }
                          />
                        ) : (
                          empleado.cod_area
                        )}
                      </td>
                      <td>
                        {editingEmpleadosId === empleado.cod_empleado ? (
                          <input
                            className="input-editar"
                            type="text"
                            name="cod_tipo_contrato"
                            value={editedEmpleadosData.cod_tipo_contrato || ""}
                            onChange={(e) =>
                              setEditedEmpleadosData({
                                ...editedEmpleadosData,
                                cod_tipo_contrato: e.target.value,
                              })
                            }
                          />
                        ) : (
                          empleado.cod_tipo_contrato
                        )}
                      </td>
                      <td> {empleado.fecha_salida}</td>
                      <td> {empleado.motivo_salida}</td>
                      <td>
                        {editingEmpleadosId === empleado.cod_empleado ? (
                          <input
                            className="input-editar"
                            type="text"
                            name="fecha_contratacion"
                            value={editedEmpleadosData.fecha_contratacion || ""}
                            onChange={(e) =>
                              setEditedEmpleadosData({
                                ...editedEmpleadosData,
                                fecha_contratacion: e.target.value,
                              })
                            }
                          />
                        ) : (
                          empleado.fecha_contratacion
                        )}
                      </td>
                      <td>
                        {editingEmpleadosId === empleado.cod_empleado ? (
                          <input
                            className="input-editar"
                            type="text"
                            name="salario"
                            value={editedEmpleadosData.salario || ""}
                            onChange={(e) =>
                              setEditedEmpleadosData({
                                ...editedEmpleadosData,
                                salario: e.target.value,
                              })
                            }
                          />
                        ) : (
                          empleado.salario
                        )}
                      </td>
                      <td>
                        {editingEmpleadosId === empleado.cod_empleado ? (
                          <input
                            className="input-editar"
                            type="text"
                            name="estado_empleado"
                            value={editedEmpleadosData.estado_empleado || ""}
                            onChange={(e) =>
                              setEditedEmpleadosData({
                                ...editedEmpleadosData,
                                estado_empleado: e.target.value,
                              })
                            }
                          />
                        ) : (
                          empleado.estado_empleado
                        )}
                      </td>
                      <td>
                        {editingEmpleadosId === empleado.cod_empleado ? (
                          <>
                            {tienePermiso("actualizar_empleados") && (
                              <button
                                onClick={handleSaveClick}
                                className="new-empleados-save-btn"
                              >
                                <FaSave />
                                Guardar
                              </button>
                            )}
                            <button
                              className="new-empleados-cancel-btn"
                              onClick={() => setEditingEmpleadosId(null)}
                            >
                              {" "}
                              <MdCancel />
                              Cancelar{" "}
                            </button>
                          </>
                        ) : (
                          <>
                            {tienePermiso("editar_empleados") && (
                              <button
                                className="new-empleados-edit-btn"
                                onClick={() => handleEditClick(empleado)}
                              >
                                <FaEdit />
                                Editar
                              </button>
                            )}
                            {tienePermiso("eliminar_empleados") && (
                              <button
                                className="new-empleados-delete-btn"
                                onClick={() =>
                                  handleDelete(empleado.cod_empleado)
                                }
                              >
                                <MdDelete />
                                Eliminar
                              </button>
                            )}
                            {tienePermiso("despedir_empleados") && (
                               <button
                                  className="btn-btn-warning-btn-sm"
                                  onClick={() => handleDespedirEmpleado(empleado)}
                                >
                                  Despedir
                                </button>
                              )}
                          </>
                        )}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="11">No hay personas disponibles.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
        <Outlet />
      </div>
    </div>
  );
};

export default GestionEmpleados;
