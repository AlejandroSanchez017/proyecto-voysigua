import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { FaSave, FaEdit } from "react-icons/fa";
import { MdDelete, MdCancel } from "react-icons/md";
import "./GestionUsuarios.css";
import Swal from "sweetalert2";
import Adminlte from "./adminlte";
import { tienePermiso } from "../Utils/permisos"; // ajusta la ruta según tu estructura

const MyComponent = () => {
  const [textoFiltro, setTextoFiltro] = useState("");
  const [usuarios, setUsuarios] = useState([]);
  const [error, setError] = useState(null);
  const location = useLocation();
  const [cantidad, setCantidad] = useState(3);
  const [editingUserId, setEditingUserId] = useState(null);
  const [editedUserData, setEditedUserData] = useState({});
  const [paginaActual, setPaginaActual] = useState(1);

  useEffect(() => {
    if (location.pathname === "/Gestion_Usuario") {
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
    const fetchUsuarios = async () => {
      try {
        const response = await fetch('${process.env.REACT_APP_API_URL}/usuarios/');
        const data = await response.json();
        setUsuarios(data);
      } catch (error) {
        console.error("Error al cargar usuarios:", error);
        setError("Error al cargar usuarios");
      }
    };
    fetchUsuarios();
  }, []);

  const handleEditClick = (usuario) => {
    setEditingUserId(usuario.id);
    setEditedUserData(usuario);
  };

  const handleSaveClick = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/usuarios/${editingUserId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(editedUserData),
        }
      );

      if (!response.ok) {
        throw new Error("Error al actualizar el usuario");
      }

      const fetchUpdatedUsuarios = async () => {
        const response = await fetch('${process.env.REACT_APP_API_URL}/usuarios/');
        const data = await response.json();
        setUsuarios(data);
      };
      await fetchUpdatedUsuarios();

      setEditingUserId(null);
      setEditedUserData({});

      Swal.fire({
        title: "¡Actualización exitosa!",
        text: "El usuario ha sido actualizado correctamente.",
        icon: "success",
        confirmButtonText: "OK",
      });
    } catch (error) {
      console.error("Error actualizando el usuario:", error);
      Swal.fire({
        title: "Error",
        text: "No se pudo actualizar el usuario. Inténtalo de nuevo.",
        icon: "error",
        confirmButtonText: "OK",
      });
    }
  };

  const deleteUserFromServer = async (id) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/${id}`, {
        method: "DELETE",
      });

      const responseBody = await response.text();

      if (response.ok) {
        return { success: true };
      } else {
        return {
          success: false,
          message: responseBody || "No se pudo eliminar el usuario.",
        };
      }
    } catch (error) {
      console.error("Error en la solicitud de eliminación:", error);
      return { success: false, message: "Error al conectar con el servidor." };
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await deleteUserFromServer(id);

      if (response.success) {
        setUsuarios((prevUsuarios) =>
          prevUsuarios.filter((usuario) => usuario.id !== id)
        );
        Swal.fire({
          icon: "success",
          title: "Usuario eliminado",
          text: "El usuario ha sido eliminado exitosamente.",
        });
      } else {
        throw new Error(response.message || "Error al eliminar el usuario.");
      }
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: error.message || "No se pudo eliminar el usuario.",
      });
      console.error("Error eliminando usuario:", error);
    }
  };

  const usuariosFiltradas = usuarios.filter((usuario) =>
    usuario.nombre.toLowerCase().includes(textoFiltro.toLowerCase())
  );

  const totalPaginas = Math.ceil(usuariosFiltradas.length / cantidad);
  return (
    <div>
      <Adminlte />
      <div className="content-wrapper">
        <section className="content">
          <div className="card-header">
            <div className="titulo-contenedor">
              <h3 className="card-title">MODULO DE USUARIOS</h3>
            </div>
          </div>
          {/* FILTROS DEBAJO DEL TÍTULO */}
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

          <div className="card-body">
            <table className="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Codigo de Personas</th>
                  <th>Nombre</th>
                  <th>Contraseña</th>
                  <th>Remember token</th>
                  <th>Nombre de Usuario</th>
                  <th>Estado</th>
                  <th>Primera vez</th>
                  <th>Fecha vencimiento</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {usuariosFiltradas.length > 0 ? (
                  usuariosFiltradas
                    .slice(
                      (paginaActual - 1) * cantidad,
                      paginaActual * cantidad
                    )
                    .map((usuario) => (
                      <tr key={usuario.id}>
                        <td>{usuario.id}</td>
                        <td>{usuario.cod_persona}</td>
                        <td>
                          {editingUserId === usuario.id ? (
                            <input
                              className="input-editar"
                              type="text"
                              name="nombre"
                              value={editedUserData.nombre || ""}
                              onChange={(e) =>
                                setEditedUserData({
                                  ...editedUserData,
                                  nombre: e.target.value,
                                })
                              }
                            />
                          ) : (
                            usuario.nombre
                          )}
                        </td>
                        <td>
                          {editingUserId === usuario.id ? (
                            <input
                              className="input-editar"
                              type="text"
                              name="password"
                              value={editedUserData.password || ""}
                              onChange={(e) =>
                                setEditedUserData({
                                  ...editedUserData,
                                  password: e.target.value,
                                })
                              }
                            />
                          ) : (
                            "*******"
                          )}
                        </td>
                        <td> {usuario.remember_token}</td>
                        <td>
                          {editingUserId === usuario.id ? (
                            <input
                              className="input-editar"
                              type="text"
                              name="username"
                              value={editedUserData.username || ""}
                              onChange={(e) =>
                                setEditedUserData({
                                  ...editedUserData,
                                  username: e.target.value,
                                })
                              }
                            />
                          ) : (
                            usuario.username
                          )}
                        </td>
                        <td>
                          {editingUserId === usuario.id ? (
                            <input
                              className="input-editar"
                              type="number"
                              name="estado"
                              value={editedUserData.estado || ""}
                              onChange={(e) =>
                                setEditedUserData({
                                  ...editedUserData,
                                  estado: e.target.value,
                                })
                              }
                            />
                          ) : (
                            usuario.estado
                          )}
                        </td>
                        <td> {usuario.primera_vez} </td>
                        <td> {usuario.fecha_vencimiento} </td>
                        <td>
                          {editingUserId === usuario.id ? (
                            <>
                              {tienePermiso("actualizar_usuarios") && (
                                <button
                                  onClick={handleSaveClick}
                                  className="new-user-save-btn"
                                >
                                  <FaSave /> Guardar{" "}
                                </button>
                              )}
                              {tienePermiso("cancelar_usuarios") && (
                                <button
                                  className="new-user-cancel-btn"
                                  onClick={() => setEditingUserId(null)}
                                >
                                  <MdCancel /> Cancelar
                                </button>
                              )}
                            </>
                          ) : (
                            <>
                              {tienePermiso("editar_usuarios") && (
                                <button
                                  className="new-user-edit-btn"
                                  onClick={() => handleEditClick(usuario)}
                                >
                                  <FaEdit /> Editar
                                </button>
                              )}
                              {tienePermiso("eliminar_usuarios") && (
                                <button
                                  className="new-user-delete-btn"
                                  onClick={() => handleDelete(usuario.id)}
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
                    <td colSpan="13">No hay usuarios disponibles.</td>
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

export default MyComponent;
