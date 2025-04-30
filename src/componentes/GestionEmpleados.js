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
  const [paginaActual, setPaginaActual] = useState(1);
  const [editedData, setEditedData] = useState({});


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
        const res = await fetch(`${process.env.REACT_APP_API_URL}/empleados/`);
        const data = await res.json();
        if (Array.isArray(data)) {
          setEmpleados(data);
        } else {
          setEmpleados([]);
        }
      } catch (err) {
        console.error("Error al cargar empleados:", err);
        setEmpleados([]);
      }
    };
    fetchEmpleados();
  }, []);

  const handleEditClick = (empleado) => {
    setEditingEmpleadosId(empleado.cod_empleado);
    setEditedData({ ...empleado });
  };

  const handleSaveClick = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/empleados/${editingEmpleadosId}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(editedData), // ✅ usamos editedData que sí se actualiza
        }
      );
  
      if (!response.ok) throw new Error("Error al actualizar el Empleado");
  
      const updated = await fetch(`${process.env.REACT_APP_API_URL}/empleados/`);
      const data = await updated.json();
      setEmpleados(data);
      setEditingEmpleadosId(null);
      setEditedData({}); // limpia el estado luego de guardar
  
      Swal.fire("Actualizado", "Empleado actualizado exitosamente", "success");
    } catch (error) {
      console.error("Error actualizando empleado:", error);
      Swal.fire("Error", "No se pudo actualizar el empleado", "error");
    }
  };
  

  const deleteEmpleadosFromServer = async (cod_empleado) => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/empleados/${cod_empleado}`,
        { method: "DELETE" }
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
      return { success: false, message: "Error al conectar con el servidor." };
    }
  };

  const handleDelete = async (cod_empleado) => {
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
      try {
        const response = await deleteEmpleadosFromServer(cod_empleado);

        if (response.success) {
          setEmpleados((prev) =>
            prev.filter((e) => e.cod_empleado !== cod_empleado)
          );
          Swal.fire("Eliminado", "Empleado eliminado exitosamente", "success");
        } else {
          throw new Error(response.message);
        }
      } catch (error) {
        Swal.fire(
          "Error",
          error.message || "No se pudo eliminar el empleado.",
          "error"
        );
      }
    }
  };

  const handleDespedirEmpleado = async (empleado) => {
    const { value: formValues } = await Swal.fire({
      title: `Despedir empleado ${empleado.cod_empleado}`,
      html: `
        <div style="display: flex; flex-direction: column; gap: 10px;">
          <input id="fecha_salida" type="date" class="swal2-input" placeholder="Fecha de salida" style="width: 100%;"/>
          <input id="motivo_salida" type="text" class="swal2-input" placeholder="Motivo de salida" style="width: 100%;"/>
        </div>
      `,
      focusConfirm: false,
      showCancelButton: true,
      confirmButtonText: "Despedir",
      cancelButtonText: "Cancelar",
      preConfirm: () => {
        const fechaSalida = document.getElementById("fecha_salida").value;
        const motivoSalida = document.getElementById("motivo_salida").value;

        if (!fechaSalida || !motivoSalida) {
          Swal.showValidationMessage("Debes completar ambos campos.");
          return false;
        }

        return { fecha_salida: fechaSalida, motivo_salida: motivoSalida };
      },
    });

    if (formValues) {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL}/empleados/despedir/${empleado.cod_empleado}`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formValues),
          }
        );

        const result = await response.json();

        if (response.ok) {
          Swal.fire("Éxito", result.message, "success");

          // Recargar empleados después del despido
          const res = await fetch(`${process.env.REACT_APP_API_URL}/empleados/`);
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

  const totalPaginas = Math.ceil(empleadosFiltrados.length / cantidad);

  const handleInputChange = (field, value) => {
    setEditedData((prevData) => ({
      ...prevData,
      [field]: value,
    }));
  };
  
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
                placeholder="Filtrar por codigo empleado"
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
                  <th>Area</th>
                  <th>Tipo Contrato</th>
                  <th>Fecha Salida</th>
                  <th>Motivo Salida</th>
                  <th>Fecha Contratacion</th>
                  <th>Salario</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {empleadosFiltrados.length > 0 ? (
                  empleadosFiltrados
                    .slice(
                      (paginaActual - 1) * cantidad,
                      paginaActual * cantidad
                    )
                    .map((empleado) => (
                      <tr key={empleado.cod_empleado}>
                        <td>{empleado.cod_empleado}</td>
                        <td>{empleado.cod_persona}</td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado ? (
                            <input
                              type="number"
                              value={editedData.cod_tipo_empleado}
                              onChange={(e) =>
                                handleInputChange(
                                  "cod_tipo_empleado",
                                  e.target.value
                                )
                              }
                            />
                          ) : (
                            empleado.cod_tipo_empleado
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado ? (
                            <input
                              type="number"
                              value={editedData.cod_area}
                              onChange={(e) =>
                                handleInputChange("cod_area", e.target.value)
                              }
                            />
                          ) : (
                            empleado.cod_area
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado ? (
                            <input
                              type="number"
                              value={editedData.cod_tipo_contrato}
                              onChange={(e) =>
                                handleInputChange(
                                  "cod_tipo_contrato",
                                  e.target.value
                                )
                              }
                            />
                          ) : (
                            empleado.cod_tipo_contrato
                          )}
                        </td>
                        <td> {empleado.fecha_salida || "-"}</td>
                        <td> {empleado.motivo_salida || "-"}</td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado ? (
                            <input
                              type="date"
                              value={editedData.fecha_contratacion || ""}
                              onChange={(e) =>
                                handleInputChange(
                                  "fecha_contratacion",
                                  e.target.value
                                )
                              }
                            />
                          ) : (
                            empleado.fecha_contratacion
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado ? (
                            <input
                              type="number"
                              value={editedData.salario}
                              onChange={(e) =>
                                handleInputChange("salario", e.target.value)
                              }
                            />
                          ) : (
                            empleado.salario
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado ? (
                            <select
                              value={editedData.estado_empleado}
                              onChange={(e) =>
                                handleInputChange(
                                  "estado_empleado",
                                  e.target.value
                                )
                              }
                            >
                              <option value="A">Activo</option>
                              <option value="I">Inactivo</option>
                            </select>
                          ) : (
                            empleado.estado_empleado
                          )}
                        </td>
                        <td>
                          {/* Botones de Guardar / Cancelar / Editar / Eliminar como ya tienes */}
                          {editingEmpleadosId === empleado.cod_empleado ? (
                            <>
                              {tienePermiso("actualizar_empleados") && (
                                <button
                                  onClick={handleSaveClick}
                                  className="new-empleados-save-btn"
                                >
                                  <FaSave /> Guardar
                                </button>
                              )}
                              <button
                                className="new-empleados-cancel-btn"
                                onClick={() => setEditingEmpleadosId(null)}
                              >
                                <MdCancel /> Cancelar
                              </button>
                            </>
                          ) : (
                            <>
                              {tienePermiso("editar_empleados") && (
                                <button
                                  className="new-empleados-edit-btn"
                                  onClick={() => handleEditClick(empleado)}
                                >
                                  <FaEdit /> Editar
                                </button>
                              )}
                              {tienePermiso("eliminar_empleados") && (
                                <button
                                  className="new-empleados-delete-btn"
                                  onClick={() =>
                                    handleDelete(empleado.cod_empleado)
                                  }
                                >
                                  <MdDelete /> Eliminar
                                </button>
                              )}
                              {tienePermiso("despedir_empleados") && (
                                <button
                                  className="new-empleados-despedir-btn"
                                  onClick={() =>
                                    handleDespedirEmpleado(empleado)
                                  }
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
                    <td colSpan="11">No hay empleados disponibles.</td>
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

export default GestionEmpleados;
