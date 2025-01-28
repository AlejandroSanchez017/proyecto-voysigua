import React, { useState, useEffect } from "react";
import { Outlet } from 'react-router-dom'; // Para renderizar rutas anidadas
import { useLocation } from "react-router-dom";
import { FaSave, FaEdit} from "react-icons/fa";
import { MdDelete, MdCancel } from "react-icons/md";
import "./GestionEmpleados.css";
import Swal from 'sweetalert2';
import Adminlte from "./adminlte";

const GestionEmpleados = () => {
  const [textoFiltro, setTextoFiltro] = useState('');
  const [empleados, setEmpleados] = useState([]);
  const [error, setError] = useState(null);
  const location = useLocation();
  const [editingEmpleadosId, setEditingEmpleadosId] = useState(null);
  const [editedEmpleadosData, setEditedEmpleadosData] = useState({});
  const [showNewEmpleadosRow, setShowNewEmpleadosRow] = useState(false);
  const [newEmpleadosData, setNewEmpleadosData] = useState({
    cod_persona: '',
    cod_tipo_empleado: '',
    cod_area:'',
    cod_tipo_contrato: '',
    fecha_salida:null,
    motivo_salida:null,
    fecha_contratacion:'',
    salario:'',
    estado_empleado:''
});


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
useEffect(() => {
    const fetchEmpleados = async () => {
      try {
        const response = await fetch("http://localhost:8000/empleados");
        const data = await response.json();
        setEmpleados(data);
      } catch (error) {
        console.error("Error al cargar Empleados:", error);
        setError("Error al cargar Empleados");
      }
    };
    fetchEmpleados();
  }, []);

//Edit
const handleEditClick = (empleado) => {
    setEditingEmpleadosId(empleado.cod_empleado);
    setEditedEmpleadosData(empleado);
  };

//guardar
const handleSaveClick = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/empleados/${editingEmpleadosId}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(editedEmpleadosData),
        }
      );
  
      if (!response.ok) {
        throw new Error('Error al actualizar el Empleado');
      }
  
      // Fuerza la recarga de los datos desde el servidor
      const fetchUpdatedEmpleados = async () => {
        const response = await fetch("http://localhost:8000/empleados");
        const data = await response.json();
        setEmpleados(data);
      };
      await fetchUpdatedEmpleados();
  
      setEditingEmpleadosId(null);
      setEditedEmpleadosData({});
  
      // Mostrar alerta de éxito
      Swal.fire({
        title: '¡Actualización exitosa!',
        text: 'El Empleado ha sido actualizado correctamente.',
        icon: 'success',
        confirmButtonText: 'OK',
      });
    } catch (error) {
      console.error('Error actualizando el empleado:', error);
  
      // Mostrar alerta de error
      Swal.fire({
        title: 'Error',
        text: 'No se pudo actualizar el empleado. Inténtalo de nuevo.',
        icon: 'error',
        confirmButtonText: 'OK',
      });
    }
  };
  
  //eliminar
const deleteEmpleadosFromServer = async (cod_empleado) => {
    try {
      const response = await fetch(`http://localhost:8000/empleados/${cod_empleado}`, {
        method: 'DELETE',
      });
  
      console.log("Response status:", response.status);  // Imprime el estado de la respuesta
      const responseBody = await response.text();  // Intentamos obtener el cuerpo de la respuesta como texto
      console.log("Response body:", responseBody);   // Imprime el cuerpo de la respuesta
  
      if (response.ok) {
        return { success: true };
      } else {
        return { success: false, message: responseBody || "No se pudo eliminar el empleado." };
      }
    } catch (error) {
      console.error("Error en la solicitud de eliminación:", error);
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
      cancelButtonText: "Cancelar"
    });
  
    if (result.isConfirmed) {
      try {
        const response = await deleteEmpleadosFromServer(cod_empleado);
  
        if (response.success) {
          setEmpleados((prevEmpleados) => 
            prevEmpleados.filter((empleado) => empleado.cod_empleado !== cod_empleado)
          );
          Swal.fire({
            icon: "success",
            title: "Empleado eliminado",
            text: "El Empleado ha sido eliminado exitosamente.",
          });
        } else {
          throw new Error(response.message || "Error al eliminar la empleado.");
        }
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Error",
          text: error.message || "No se pudo eliminar la empleado.",
        });
        console.error("Error eliminando la empleado:", error);
      }
    }
  };  

//Guardar datos
const handleSaveNewEmpleados = async () => {
  try {
    // Mostrar en consola los datos que se enviarán al servidor
    console.log("Datos a enviar:", newEmpleadosData);

    // Enviar datos al servidor para guardar el nuevo empleado
    const response = await fetch('http://localhost:8000/empleados/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newEmpleadosData),
    });

    // Verificar si la respuesta es exitosa
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error al guardar:', errorData); // Mostrar el error recibido del servidor
      throw new Error('Error al guardar el empleado en la base de datos');
    }

    // Mostrar en consola la respuesta completa del servidor
    console.log("Respuesta del servidor:", response);

    const result = await response.json();

    // Mostrar en consola el resultado JSON recibido del servidor
    console.log("Datos guardados en la base de datos:", result);

    // Si la respuesta fue exitosa, actualizar el estado de los empleados
    setEmpleados((prevEmpleados) => [
      ...prevEmpleados,
      { ...newEmpleadosData, cod_empleado: prevEmpleados.length + 1 },
    ]);

    // Limpiar el estado de newEmpleadosData y ocultar el formulario
    setNewEmpleadosData({
        cod_persona: '',
        cod_tipo_empleado: '',
        cod_area:'',
        cod_tipo_contrato: '',
        fecha_salida:'',
        motivo_salida:'',
        fecha_contratacion:'',
        salario:'',
        estado_empleado:''
    });
    setShowNewEmpleadosRow(false);  // Ocultar la fila de "Agregar nuevo empleado"

    // Mostrar mensaje de éxito
    Swal.fire({
      icon: "success",
      title: "empleado guardado",
      text: "el empleado se ha guardado exitosamente.",
      confirmButtonColor: "#3085d6",
      confirmButtonText: "OK"
    });
  } catch (error) {
    console.error('Error:', error);
    Swal.fire({
      icon: "error",
      title: "Error al guardar el empleado",
      text: error.message,
      confirmButtonColor: "#d33",
      confirmButtonText: "OK"
    });
  }
};

// Filtrar datos
const empleadosFiltrados = empleados.filter(empleado =>
  empleado.cod_empleado.toString().includes(textoFiltro)  // Convertir a cadena si es necesario
);

return (
    <div className="content-wrapper">
        <Adminlte />
      <section className="content-header">
        <h1>Gestión de Empleados</h1>
      </section>
      <section className="content">
        <div className="container-fluid">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Lista de Empleados</h3>
              <div className="button-container">
              <button onClick={() => setShowNewEmpleadosRow(true)} className="agregar-empleado-btn">
                Agregar empleado
              </button>
            </div>
            </div>
            <div className="card-body">
            <input
                type="text"
                placeholder="Filtrar por codigo empleado"
                value={textoFiltro}
                onChange={(e) => setTextoFiltro(e.target.value)}
                className="filter-input"
              />
              {error && <p style={{ color: "red" }}>Error: {error}</p>}
              <table className="table table-bordered table-striped">
                <thead>
                  <tr>
                    <th>cod_empleado</th>
                    <th>Persona</th>
                    <th>Tipo empleado</th>
                    <th>Area</th>
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
                      <input type="number" className="new-empleados-input" value={newEmpleadosData.cod_persona} onChange={(e) => setNewEmpleadosData({ ...newEmpleadosData, cod_persona: e.target.value })} />
                    </td>
                    <td className="new-empleados-cell">
                      <input type="number" className="new-empleados-input" value={newEmpleadosData.cod_tipo_empleado} onChange={(e) => setNewEmpleadosData({ ...newEmpleadosData, cod_tipo_empleado: e.target.value })} />
                    </td>
                    <td className="new-empleados-cell">
                      <input type="number" className="new-empleados-input" value={newEmpleadosData.cod_area} onChange={(e) => setNewEmpleadosData({ ...newEmpleadosData, cod_area: e.target.value })} />
                    </td>
                    <td className="new-empleados-cell">
                      <input type="number" className="new-empleados-input" value={newEmpleadosData.cod_tipo_contrato} onChange={(e) => setNewEmpleadosData({ ...newEmpleadosData, cod_tipo_contrato: e.target.value })} />
                    </td>
                    <td className="new-empleados-cell">
                      <input type="date" className="new-empleados-input" value={newEmpleadosData.fecha_salida} onChange={(e) => setNewEmpleadosData({ ...newEmpleadosData, fecha_salida: e.target.value })} />
                    </td>
                    <td className="new-empleados-cell">
                      <input type="text" className="new-empleados-input" value={newEmpleadosData.motivo_salida} onChange={(e) => setNewEmpleadosData({ ...newEmpleadosData, motivo_salida: e.target.value })} />
                    </td>
                    <td className="new-empleados-cell">
                      <input type="date" className="new-empleados-input" value={newEmpleadosData.fecha_contratacion} onChange={(e) => setNewEmpleadosData({ ...newEmpleadosData, fecha_contratacion: e.target.value })} />
                    </td>
                    <td className="new-empleados-cell">
                      <input type="number" className="new-empleados-input" value={newEmpleadosData.salario} onChange={(e) => setNewEmpleadosData({ ...newEmpleadosData, salario: e.target.value })} />
                    </td>
                    <td className="new-empleados-cell">
                      <input type="text" className="new-empleados-input" value={newEmpleadosData.estado_empleado} onChange={(e) => setNewEmpleadosData({ ...newEmpleadosData, estado_empleado: e.target.value })} />
                    </td>
                    <td className="new-empleados-cell">
                      <button onClick={handleSaveNewEmpleados} className="new-empleados-save-btn"><FaSave />Guardar</button>
                      <button onClick={() => setShowNewEmpleadosRow(false)} className="new-empleados-cancel-btn"><MdCancel />Cancelar</button>
                    </td>
                  </tr>
                )}
                  {empleadosFiltrados.length > 0 ? (
                    empleadosFiltrados.map((empleado) => (
                      <tr key={empleado.cod_empleado}>
                        <td>{empleado.cod_empleado}</td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado ? (
                            <input className="input-editar" type="number" name="cod_persona" value={editedEmpleadosData.cod_persona || ''} onChange={(e) => setEditedEmpleadosData({ ...editedEmpleadosData, cod_persona: e.target.value })} />
                          ) : (
                            empleado.cod_persona
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado? (
                            <input className="input-editar" type="text" name="cod_tipo_empleado" value={editedEmpleadosData.cod_tipo_empleado || ''} onChange={(e) =>setEditedEmpleadosData({ ...editedEmpleadosData, cod_tipo_empleado: e.target.value })}/>
                          ) : (
                            empleado.cod_tipo_empleado
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado? (
                            <input className="input-editar" type="text" name="cod_area" value={editedEmpleadosData.cod_area || ''} onChange={(e) => setEditedEmpleadosData({ ...editedEmpleadosData, cod_area: e.target.value }) }/>
                          ) : (
                            empleado.cod_area
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado? (
                            <input className="input-editar" type="text" name="cod_tipo_contrato" value={editedEmpleadosData.cod_tipo_contrato || ''} onChange={(e) => setEditedEmpleadosData({ ...editedEmpleadosData, cod_tipo_contrato: e.target.value })}/>
                          ) : (
                            empleado.cod_tipo_contrato
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado? (
                            <input className="input-editar" type="date" name="fecha_salida" value={editedEmpleadosData.fecha_salida || ''} onChange={(e) => setEditedEmpleadosData({ ...editedEmpleadosData, fecha_salida: e.target.value })} />
                          ) : (
                            empleado.fecha_salida
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado? (
                            <input className="input-editar" type="text" name="motivo_salida" value={editedEmpleadosData.motivo_salida || ''} onChange={(e) =>setEditedEmpleadosData({ ...editedEmpleadosData, motivo_salida: e.target.value })}/>
                          ) : (
                            empleado.motivo_salida
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado? (
                            <input className="input-editar" type="text" name="fecha_contratacion" value={editedEmpleadosData.fecha_contratacion|| ''} onChange={(e) => setEditedEmpleadosData({ ...editedEmpleadosData, fecha_contratacion: e.target.value })} />
                          ) : (
                            empleado.fecha_contratacion
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado? (
                            <input className="input-editar" type="text" name="salario" value={editedEmpleadosData.salario|| ''} onChange={(e) => setEditedEmpleadosData({ ...editedEmpleadosData, salario: e.target.value }) }/>
                          ) : (
                            empleado.salario
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado? (
                            <input className="input-editar" type="text" name="estado_empleado" value={editedEmpleadosData.estado_empleado|| ''} onChange={(e) => setEditedEmpleadosData({ ...editedEmpleadosData, estado_empleado: e.target.value }) }/>
                          ) : (
                            empleado.estado_empleado
                          )}
                        </td>
                        <td>
                          {editingEmpleadosId === empleado.cod_empleado? (
                            <>
                              <button onClick={handleSaveClick} className="new-empleados-save-btn"><FaSave />Guardar</button>
                              <button className="new-empleados-cancel-btn" onClick={() => setEditingEmpleadosId(null)}>{" "}<MdCancel />Cancelar{" "}</button>
                            </>
                          ) : (
                            <>
                            <button className="new-empleados-edit-btn" onClick={() => handleEditClick(empleado)}><FaEdit />Editar</button>
                            <button className="new-empleados-delete-btn" onClick={() => handleDelete(empleado.cod_empleado)}><MdDelete />Eliminar</button>
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
  );
};

export default GestionEmpleados;