import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { FaSave, FaEdit} from "react-icons/fa";
import { MdDelete, MdCancel } from "react-icons/md";
import "./MyComponent.css";
import Swal from 'sweetalert2';
import Adminlte from "./adminlte";

const MyComponent = () => {
  const [textoFiltro, setTextoFiltro] = useState('');
  const [usuarios, setUsuarios] = useState([]);
  const [error, setError] = useState(null);
  const location = useLocation();
  const [editingUserId, setEditingUserId] = useState(null);
  const [editedUserData, setEditedUserData] = useState({});
  const [showNewUserRow, setShowNewUserRow] = useState(false);
  const [newUserData, setNewUserData] = useState({
  cod_persona: "",
  nombre: "",
  password: "",
  token: "",
  username: "",
  estado: 1,
  primera_vez: false,
  fecha_vencimiento: "",
});


  // Cargar el script solo en la página de Gestión Usuario
  useEffect(() => {
    if (location.pathname === "/Gestion_Usuario") {
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

  // Cargar usuarios al iniciar
  useEffect(() => {
    const fetchUsuarios = async () => {
      try {
        const response = await fetch("http://localhost:8000/usuarios/");
        const data = await response.json();
        setUsuarios(data);
      } catch (error) {
        console.error("Error al cargar usuarios:", error);
        setError("Error al cargar usuarios");
      }
    };
    fetchUsuarios();
  }, []);

//Edit
  const handleEditClick = (usuario) => {
    setEditingUserId(usuario.id);
    setEditedUserData(usuario);
  };

//guardar
  const handleSaveClick = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/usuarios/${editingUserId}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(editedUserData),
        }
      );
  
      if (!response.ok) {
        throw new Error('Error al actualizar el usuario');
      }
  
      // Fuerza la recarga de los datos desde el servidor
      const fetchUpdatedUsuarios = async () => {
        const response = await fetch("http://localhost:8000/usuarios/");
        const data = await response.json();
        setUsuarios(data);
      };
      await fetchUpdatedUsuarios();
  
      setEditingUserId(null);
      setEditedUserData({});
  
      // Mostrar alerta de éxito
      Swal.fire({
        title: '¡Actualización exitosa!',
        text: 'El usuario ha sido actualizado correctamente.',
        icon: 'success',
        confirmButtonText: 'OK',
      });
    } catch (error) {
      console.error('Error actualizando el usuario:', error);
  
      // Mostrar alerta de error
      Swal.fire({
        title: 'Error',
        text: 'No se pudo actualizar el usuario. Inténtalo de nuevo.',
        icon: 'error',
        confirmButtonText: 'OK',
      });
    }
  };
  
  //eliminar
  const deleteUserFromServer = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/usuarios/${id}`, {
        method: 'DELETE',
      });
  
      console.log("Response status:", response.status);  // Imprime el estado de la respuesta
      const responseBody = await response.text();  // Intentamos obtener el cuerpo de la respuesta como texto
      console.log("Response body:", responseBody);   // Imprime el cuerpo de la respuesta
  
      if (response.ok) {
        return { success: true };
      } else {
        return { success: false, message: responseBody || "No se pudo eliminar el usuario." };
      }
    } catch (error) {
      console.error("Error en la solicitud de eliminación:", error);
      return { success: false, message: "Error al conectar con el servidor." };
    }
  };
//eliminar
const handleDelete = async (id) => {
  try {
    const response = await deleteUserFromServer(id);

    if (response.success) {
      setUsuarios((prevUsuarios) => prevUsuarios.filter((usuario) => usuario.id !== id));  // Actualiza el estado de los usuarios
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

//Guardar datos
const handleSaveNewUser = async () => {
  try {
    // Mostrar en consola los datos que se enviarán al servidor
    console.log("Datos a enviar:", newUserData);

    // Enviar datos al servidor para guardar el nuevo usuario
    const response = await fetch('http://localhost:8000/usuarios/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newUserData),
    });

    // Verificar si la respuesta es exitosa
    if (!response.ok) {
      const errorDetails = await response.text(); // Mostrar más detalles del error
      console.error('Error al guardar el usuario:', errorDetails);
      throw new Error('Error al guardar el usuario en la base de datos');
    }

    const result = await response.json();
    console.log("Datos guardados en la base de datos:", result);

    // Actualizar el estado de los usuarios con la respuesta del backend
    setUsuarios((prevUsuarios) => [
      ...prevUsuarios,
      { ...newUserData, id: result.id || prevUsuarios.length + 1 }, // Usar el id del backend
    ]);

    // Limpiar el estado de newUserData y ocultar el formulario
    setNewUserData({
      cod_persona: "",
      nombre: "",
      password: "",
      token: "",
      username: "",
      estado: 1,
      primera_vez: false,
      fecha_vencimiento: "",
    });
    setShowNewUserRow(false);  // Ocultar la fila de "Agregar nuevo usuario"

    // Mostrar mensaje de éxito
    Swal.fire({
      icon: "success",
      title: "Usuario guardado",
      text: "El usuario se ha guardado exitosamente.",
      confirmButtonColor: "#3085d6",
      confirmButtonText: "OK"
    });
  } catch (error) {
    console.error('Error:', error);
    Swal.fire({
      icon: "error",
      title: "Error al guardar el usuario",
      text: error.message,
      confirmButtonColor: "#d33",
      confirmButtonText: "OK"
    });
  }
};

// Filter personas based on filter text
const usuariosFiltradas = usuarios.filter(usuario =>
  usuario.nombre.toLowerCase().includes(textoFiltro.toLowerCase())
);
  
  return (
    <div>
      <Adminlte />
      <div className="content-wrapper">  
        <h1> </h1>
      <section className="content">
        <div className="container-fluid">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">GESTION DE USUARIOS</h3>           
            </div>
            <div  className="button-container">
            <button onClick={() => setShowNewUserRow(true)} className="agregar-usuario-btn">
                Agregar Usuario
            </button>
            </div>
            <input
                type="text"
                placeholder="Filtrar por Nombre..."
                value={textoFiltro}
                onChange={(e) => setTextoFiltro(e.target.value)}
                className="filter-input"
              />
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
                {showNewUserRow && (
                    <tr className="new-user-row">
                    <td className="new-user-cell">Nuevo Usuario</td>
                    <td className="new-user-cell">
                      <input type="number" className="new-user-input" value={newUserData.cod_persona} onChange={(e) => setNewUserData({ ...newUserData, cod_persona: e.target.value })} />
                    </td>
                    <td className="new-user-cell">
                      <input type="text" className="new-user-input" value={newUserData.nombre} onChange={(e) => setNewUserData({ ...newUserData, nombre: e.target.value })} />
                    </td>
                    <td className="new-user-cell">
                      <input type="text" className="new-user-input" value={newUserData.password} onChange={(e) => setNewUserData({ ...newUserData, password: e.target.value })} />
                    </td>
                    <td className="new-user-cell">
                      <input type="text" className="new-user-input" value={newUserData.remember_token} onChange={(e) => setNewUserData({ ...newUserData, remember_token: e.target.value })} />
                    </td>
                    <td className="new-user-cell">
                      <input type="text" className="new-user-input" value={newUserData.username} onChange={(e) => setNewUserData({ ...newUserData, username: e.target.value })} />
                    </td>
                    <td className="new-user-cell">
                      <input type="number" className="new-user-input" value={newUserData.estado} onChange={(e) => setNewUserData({ ...newUserData, estado: e.target.value })} />
                    </td>
                    <td className="new-user-cell">
                      <input type="checkbox" className="new-user-checkbox" checked={newUserData.primera_vez} onChange={(e) => setNewUserData({ ...newUserData, primera_vez: e.target.checked })} />
                    </td>
                    <td className="new-user-cell">
                      <input type="date" className="new-user-input" value={newUserData.fecha_vencimiento} onChange={(e) => setNewUserData({ ...newUserData, fecha_vencimiento: e.target.value })} />
                    </td>
                    <td className="new-user-cell">
                      <button onClick={handleSaveNewUser} className="new-user-save-btn"><FaSave />Guardar</button>
                      <button onClick={() => setShowNewUserRow(false)} className="new-user-cancel-btn"><MdCancel />Cancelar</button>
                    </td>
                  </tr>
                )}
                  {usuariosFiltradas.length > 0 ? (
                    usuariosFiltradas.map((usuario) => (
                      <tr key={usuario.id}>
                        <td>{usuario.id}</td>
                        <td>{usuario.cod_persona}</td>
                        <td>
                          {editingUserId === usuario.id ? (
                            <input className="input-editar" type="text" name="nombre" value={editedUserData.nombre || ''} onChange={(e) =>setEditedUserData({ ...editedUserData, nombre: e.target.value })
                            }
                            />
                          ) : (
                            usuario.nombre
                          )}
                        </td>
                        <td>
                          {editingUserId === usuario.id ? (
                            <input className="input-editar" type="text" name="password" value={editedUserData.password || ''} onChange={(e) => setEditedUserData({ ...editedUserData, password: e.target.value }) }/>
                          ) : (
                           "*******"
                          )}
                        </td>
                        <td> {usuario.remember_token}</td>
                        <td>
                          {editingUserId === usuario.id ? (
                            <input className="input-editar" type="text" name="username" value={editedUserData.username || ''} onChange={(e) => setEditedUserData({ ...editedUserData, username: e.target.value })} />
                          ) : (
                            usuario.username
                          )}
                        </td>
                        
                        <td>
                          {editingUserId === usuario.id ? (
                            <input className="input-editar" type="number" name="estado" value={editedUserData.estado || ''} onChange={(e) => setEditedUserData({ ...editedUserData, estado: e.target.value })} />
                          ) : (
                            usuario.estado
                          )}
                        </td>
                        <td> {usuario.primera_vez} </td>
                        <td> {usuario.fecha_vencimiento} </td>
                        <td>
                          {editingUserId === usuario.id ? (
                            <>
                              <button onClick={handleSaveClick} className="new-user-save-btn"><FaSave />Guardar</button>
                              <button className="new-user-cancel-btn" onClick={() => setEditingUserId(null)}>{" "}<MdCancel />Cancelar{" "}</button>
                            </>
                          ) : (
                            <>
                            <button className="new-user-edit-btn" onClick={() => handleEditClick(usuario)}><FaEdit />Editar</button>
                            <button className="new-user-delete-btn" onClick={() => handleDelete(usuario.id)}><MdDelete />Eliminar</button>
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
            </div>
          </div>
        </div>
      </section>
      </div>
    </div>
  );
};

export default MyComponent;
