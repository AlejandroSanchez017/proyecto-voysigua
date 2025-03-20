import React, { useState, useEffect } from "react";
import { Outlet } from "react-router-dom"; // Para renderizar rutas anidadas
import { useLocation } from "react-router-dom";
import { FaSave, FaEdit } from "react-icons/fa";
import { MdDelete, MdCancel } from "react-icons/md";
import { BsFillPersonXFill } from "react-icons/bs";
import "./GestionEmpleados.css";
import Swal from "sweetalert2";
import axios from "axios";
import Adminlte from "./adminlte";

const GestionEmpleados = () => {
  const [textoFiltro, setTextoFiltro] = useState("");
  const [empleados, setEmpleados] = useState([]);
  const location = useLocation();
  const [error] = useState(null);
  const [fechaSalida, setFechaSalida] = useState("");
  const [motivoSalida, setMotivoSalida] = useState("");
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

  const despedirEmpleado = async (cod_empleado) => {
    if (!fechaSalida || !motivoSalida) {
      Swal.fire("Error", "Debes ingresar fecha y motivo de salida.", "error");
      return;
    }
  
    try {
      const response = await axios.put(
        `http://localhost:8000/empleados/despedir/${cod_empleado}`,
        {
          fecha_salida: fechaSalida,
          motivo_salida: motivoSalida,
        }
      );
  
      if (response.status === 200) {
        Swal.fire("Éxito", response.data.message, "success");
  
        // 🔹 Recargar la lista de empleados
        await fetchEmpleados();
  
        // 🔹 Salir del modo edición
        setEditingEmpleadosId(null);
      } else {
        throw new Error("Error en la respuesta del servidor");
      }
  
    } catch (error) {
      Swal.fire(
        "Error",
        error.response?.data?.detail?.error || "Error al despedir empleado",
        "error"
      );
    }
  };
  

  // Cargar el script solo en la página de Gestión Empleados
  useEffect(() => {
    if (location.pathname === "/Gestion_Empleados") {
      const script = document.createElement("script");
      script.src = "/plugins/sparklines/sparkline.js";
      script.async = true;
      document.body.appendChild(script);

      // Cleanup function to remove the script on component unmount
      return () => {
        document.body.removeChild(script);
      };
    }
  }, [location]);

  // Cargar Empleados al iniciar
  const fetchEmpleados = async () => {
    try {
      const response = await fetch("http://localhost:8000/empleados/");
      const data = await response.json();
  
      console.log("Datos obtenidos del backend:", data); // 🔹 Verificar qué recibe React
  
      if (Array.isArray(data)) {
        setEmpleados(data); // 🔹 Asegurar que solo se asigna si es un array
      } else {
        console.error("La respuesta del servidor no es un array:", data);
        setEmpleados([]); // Evita que React falle
      }
    } catch (error) {
      console.error("Error al cargar empleados:", error);
      setEmpleados([]); // En caso de error, asignar un array vacío
    }
  };
  
    
    useEffect(() => {
      fetchEmpleados(); // Carga inicial de datos
    }, []);

  //Edit
  const handleEditClick = (empleado) => {
    setEditingEmpleadosId(empleado.cod_empleado);
    setEditedEmpleadosData({ ...empleado});
  };

  //guardar
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
  
      if (!response.ok) {
        throw new Error("Error al actualizar el empleado");
      }
  
      const fetchUpdatedEmpleados = async () => {
        const response = await fetch("http://localhost:8000/empleados/");
        if (!response.ok) {
          throw new Error("Error al obtener empleados actualizados");
        }
        const data = await response.json();
        console.log("Datos actualizados obtenidos:", data); // Debug
        setEmpleados([...data]); // asegura nueva referencia
        console.log("Estado actualizado en React:", data);
      };
  
      await fetchUpdatedEmpleados();
  
      setEditingEmpleadosId(null);
      setEditedEmpleadosData({});
  
      Swal.fire({
        title: "¡Actualización exitosa!",
        text: "El empleado ha sido actualizado correctamente.",
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
  
  

  //eliminar
  const deleteEmpleadosFromServer = async (cod_empleado) => {
    try {
      const response = await fetch(`http://localhost:8000/empleados/${cod_empleado}`, {
        method: "DELETE",
      });
  
      if (response.ok) {
        await fetchEmpleados();  // 🔹 Recargar la lista después de eliminar
        return { success: true };
      } else {
        return { success: false, message: "No se pudo eliminar el empleado." };
      }
    } catch (error) {
      return { success: false, message: "Error al conectar con el servidor." };
    }
  };
  
  
  //eliminar
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
          console.log("Empleado eliminado, recargando lista...");
  
          await fetchEmpleados(); // 🔹 Volver a cargar empleados
  
          Swal.fire({
            icon: "success",
            title: "Empleado eliminado",
            text: "El empleado ha sido eliminado exitosamente.",
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
      }
    }
  };
  
  

  //Guardar datos
  const handleSaveNewEmpleados = async () => {
    try {
      console.log("Datos a enviar:", newEmpleadosData);
  
      const response = await fetch("http://localhost:8000/empleados/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newEmpleadosData),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error al guardar:", errorData);
        throw new Error("Error al guardar el empleado en la base de datos");
      }
  
      const result = await response.json();
  
      console.log("Datos guardados en la base de datos:", result);
  
      // 🔹 Recargar la lista desde el servidor después de insertar
      await fetchEmpleados();
  
      setNewEmpleadosData({
        cod_persona: "",
        cod_tipo_empleado: "",
        cod_area: "",
        cod_tipo_contrato: "",
        fecha_salida: "",
        motivo_salida: "",
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

  //Filtrar datos
  const empleadosFiltrados = Array.isArray(empleados)
  ? empleados.filter(
      (empleado) =>
        empleado.cod_empleado &&
        empleado.cod_empleado.toString().includes(textoFiltro.toString())
    )
  : [];

  return (
    <div>
      <Adminlte />
      <div className="content-wrapper">
        <h1> </h1>
        <section className="content">
          <div className="container-fluid">
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">GESTION DE EMPLEADOS</h3>
              </div>
              <div className="button-container">
                <button
                  onClick={() => setShowNewEmpleadosRow(true)}
                  className="agregar-empleado-btn"
                >
                  Agregar empleado
                </button>
              </div>
              <input
                type="text"
                placeholder="Filtrar por codigo empleado"
                value={textoFiltro}
                onChange={(e) => setTextoFiltro(e.target.value)}
                className="filter-input"
              />
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
                        <td className="new-empleados-cell">
                          <input
                            type="date"
                            className="new-empleados-input"
                            value={newEmpleadosData.fecha_salida}
                            onChange={(e) =>
                              setNewEmpleadosData({
                                ...newEmpleadosData,
                                fecha_salida: e.target.value,
                              })
                            }
                          />
                        </td>
                        <td className="new-empleados-cell">
                          <input
                            type="text"
                            className="new-empleados-input"
                            value={newEmpleadosData.motivo_salida}
                            onChange={(e) =>
                              setNewEmpleadosData({
                                ...newEmpleadosData,
                                motivo_salida: e.target.value,
                              })
                            }
                          />
                        </td>
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
                          <button
                            onClick={handleSaveNewEmpleados}
                            className="new-empleados-save-btn"
                          >
                            <FaSave />
                            Guardar
                          </button>
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
                                value={
                                  editedEmpleadosData.cod_tipo_empleado || ""
                                }
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
                                value={
                                  editedEmpleadosData.cod_tipo_contrato || ""
                                }
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
                          <td>
                            {editingEmpleadosId === empleado.cod_empleado ? (
                              <input
                              type="date"
                              value={fechaSalida}
                              onChange={(e) => setFechaSalida(e.target.value)}
                            />
                            ) : (
                              empleado.fecha_salida
                            )}
                          </td>
                          <td>
                            {editingEmpleadosId === empleado.cod_empleado ? (
                              <input
                              type="text"
                              placeholder="Motivo salida"
                              value={motivoSalida}
                              onChange={(e) => setMotivoSalida(e.target.value)}
                            />
                            ) : (
                              empleado.motivo_salida
                            )}
                          </td>

                          <td>
                            {editingEmpleadosId === empleado.cod_empleado ? (
                              <input
                                className="input-editar"
                                type="text"
                                name="fecha_contratacion"
                                value={
                                  editedEmpleadosData.fecha_contratacion || ""
                                }
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
                                value={
                                  editedEmpleadosData.estado_empleado || ""
                                }
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
                                <button
                                  onClick={handleSaveClick}
                                  className="new-empleados-save-btn"
                                >
                                  <FaSave />
                                  Guardar
                                </button>
                                <button
                                  className="new-empleados-despedir-btn"
                                  onClick={() => despedirEmpleado(empleado.cod_empleado)}
                                >
                                  <BsFillPersonXFill />
                                  Despedir 
                                </button>
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
                                <button
                                  className="new-empleados-edit-btn"
                                  onClick={() => handleEditClick(empleado)}
                                >
                                  <FaEdit />
                                  Editar
                                </button>
                                
                                <button
                                  className="new-empleados-delete-btn"
                                  onClick={() =>
                                    handleDelete(empleado.cod_empleado)
                                  }
                                >
                                  <MdDelete />
                                  Eliminar
                                </button>
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
            </div>
          </div>
        </section>
        <Outlet />
      </div>
    </div>
  );
};

export default GestionEmpleados;
