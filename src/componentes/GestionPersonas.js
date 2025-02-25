import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { FaSave, FaEdit} from "react-icons/fa";
import { MdDelete, MdCancel } from "react-icons/md";
import "./GestionPersonas.css";
import Swal from 'sweetalert2';
import Adminlte from "./adminlte";

const GestionPersonas = () => {
  const [textoFiltro, setTextoFiltro] = useState('');
  const [personas, setPersonas] = useState([]);
  const [error, setError] = useState(null);
  const location = useLocation();
  const [editingPersonasId, setEditingPersonasId] = useState(null);
  const [editedPersonasData, setEditedPersonasData] = useState({});
  const [showNewPersonasRow, setShowNewPersonasRow] = useState(false);
  const [newPersonasData, setNewPersonasData] = useState({
  cod_tipo_persona: '',
  dni: '',
  primer_nombre: '',
  apellido: '',
  fecha_nacimiento: '',
  sexo: '',
  correo: '',
  estado: ''
});


  // Cargar el script solo en la página de Gestión Personas
  useEffect(() => {
    if (location.pathname === "/Gestion_Personas") {
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

  // Cargar Personas al iniciar
useEffect(() => {
    const fetchPersonas = async () => {
      try {
        const response = await fetch("http://localhost:8000/personas");
        const data = await response.json();
        setPersonas(data);
      } catch (error) {
        console.error("Error al cargar Personas:", error);
        setError("Error al cargar Personas");
      }
    };
    fetchPersonas();
  }, []);

//Edit
const handleEditClick = (persona) => {
    setEditingPersonasId(persona.cod_persona);
    setEditedPersonasData(persona);
  };

//guardar
const handleSaveClick = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/personas/${editingPersonasId}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(editedPersonasData),
        }
      );
  
      if (!response.ok) {
        throw new Error('Error al actualizar el persona');
      }
  
      // Fuerza la recarga de los datos desde el servidor
      const fetchUpdatedPersonas = async () => {
        const response = await fetch("http://localhost:8000/personas");
        const data = await response.json();
        setPersonas(data);
      };
      await fetchUpdatedPersonas();
  
      setEditingPersonasId(null);
      setEditedPersonasData({});
  
      // Mostrar alerta de éxito
      Swal.fire({
        title: '¡Actualización exitosa!',
        text: 'El persona ha sido actualizado correctamente.',
        icon: 'success',
        confirmButtonText: 'OK',
      });
    } catch (error) {
      console.error('Error actualizando el persona:', error);
  
      // Mostrar alerta de error
      Swal.fire({
        title: 'Error',
        text: 'No se pudo actualizar el persona. Inténtalo de nuevo.',
        icon: 'error',
        confirmButtonText: 'OK',
      });
    }
  };
  
  //eliminar
const deletePersonasFromServer = async (cod_persona) => {
    try {
      const response = await fetch(`http://localhost:8000/personas/${cod_persona}`, {
        method: 'DELETE',
      });
  
      console.log("Response status:", response.status);  // Imprime el estado de la respuesta
      const responseBody = await response.text();  // Intentamos obtener el cuerpo de la respuesta como texto
      console.log("Response body:", responseBody);   // Imprime el cuerpo de la respuesta
  
      if (response.ok) {
        return { success: true };
      } else {
        return { success: false, message: responseBody || "No se pudo eliminar el persona." };
      }
    } catch (error) {
      console.error("Error en la solicitud de eliminación:", error);
      return { success: false, message: "Error al conectar con el servidor." };
    }
  };
//eliminar
const handleDelete = async (cod_persona) => {
  const result = await Swal.fire({
    title: "¿Estás seguro?",
    text: "Esta acción no se puede deshacer. ¿Deseas eliminar la persona?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar"
  });

  if (result.isConfirmed) {
    try {
      const response = await deletePersonasFromServer(cod_persona);

      if (response.success) {
        setPersonas((prevPersonas) => 
          prevPersonas.filter((persona) => persona.cod_persona !== cod_persona)
        );
        Swal.fire({
          icon: "success",
          title: "Persona eliminada",
          text: "La Persona ha sido eliminado exitosamente.",
        });
      } else {
        throw new Error(response.message || "Error al eliminar la Persona.");
      }
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: error.message || "No se pudo eliminar la Persona.",
      });
      console.error("Error eliminando la persona:", error);
    }
  }
}; 

//Guardar datos
const handleSaveNewPersonas = async () => {
  try {
    // Mostrar en consola los datos que se enviarán al servidor
    console.log("Datos a enviar:", newPersonasData);

    // Enviar datos al servidor para guardar el nuevo persona
    const response = await fetch('http://localhost:8000/personas/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newPersonasData),
    });

    // Verificar si la respuesta es exitosa
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error al guardar:', errorData); // Mostrar el error recibido del servidor
      throw new Error('Error al guardar la persona en la base de datos');
    }

    // Mostrar en consola la respuesta completa del servidor
    console.log("Respuesta del servidor:", response);

    const result = await response.json();

    // Mostrar en consola el resultado JSON recibido del servidor
    console.log("Datos guardados en la base de datos:", result);

    // Si la respuesta fue exitosa, actualizar el estado de los personas
    setPersonas((prevPersonas) => [
      ...prevPersonas,
      { ...newPersonasData, cod_persona: prevPersonas.length + 1 },
    ]);

    // Limpiar el estado de newPersonasData y ocultar el formulario
    setNewPersonasData({
        cod_tipo_persona: "",
        dni: "",
        primer_nombre: "",
        apellido: "",
        fecha_nacimiento: "",
        sexo: "",
        correo: "",
        estado: "",
    });
    setShowNewPersonasRow(false);  // Ocultar la fila de "Agregar nuevo persona"

    // Mostrar mensaje de éxito
    Swal.fire({
      icon: "success",
      title: "Persona guardado",
      text: "La Persona se ha guardado exitosamente.",
      confirmButtonColor: "#3085d6",
      confirmButtonText: "OK"
    });
  } catch (error) {
    console.error('Error:', error);
    Swal.fire({
      icon: "error",
      title: "Error al guardar la persona",
      text: error.message,
      confirmButtonColor: "#d33",
      confirmButtonText: "OK"
    });
  }
};

 // Filter personas based on filter text
 const personasFiltradas = personas.filter(persona =>
  persona.primer_nombre.toLowerCase().includes(textoFiltro.toLowerCase())
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
              <h3 className="card-title">GESTION DE PERSONAS</h3>
            </div>
            <div className="button-container">
              <button onClick={() => setShowNewPersonasRow(true)} className="agregar-persona-btn">
                Agregar Persona
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
                    <th>Codigo de persona</th>
                    <th>Codigo Tipo Persona</th>
                    <th>Dni</th>
                    <th>Nombres</th>
                    <th>Apellidos</th>
                    <th>Fecha nacimiento</th>
                    <th>Sexo</th>
                    <th>Correo</th>
                    <th>estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                {showNewPersonasRow && (
                    <tr className="new-personas-row">
                    <td className="new-personas-cell">Nueva Persona</td>
                    <td className="new-personas-cell">
                      <input type="number" className="new-personas-input" value={newPersonasData.cod_tipo_persona} onChange={(e) => setNewPersonasData({ ...newPersonasData, cod_tipo_persona: e.target.value })} />
                    </td>
                    <td className="new-personas-cell">
                      <input type="text" className="new-personas-input" value={newPersonasData.dni} onChange={(e) => setNewPersonasData({ ...newPersonasData, dni: e.target.value })} />
                    </td>
                    <td className="new-personas-cell">
                      <input type="text" className="new-personas-input" value={newPersonasData.primer_nombre} onChange={(e) => setNewPersonasData({ ...newPersonasData, primer_nombre: e.target.value })} />
                    </td>
                    <td className="new-personas-cell">
                      <input type="text" className="new-personas-input" value={newPersonasData.apellido} onChange={(e) => setNewPersonasData({ ...newPersonasData, apellido: e.target.value })} />
                    </td>
                    <td className="new-personas-cell">
                      <input type="date" className="new-personas-input" value={newPersonasData.fecha_nacimiento} onChange={(e) => setNewPersonasData({ ...newPersonasData, fecha_nacimiento: e.target.value })} />
                    </td>
                    <td className="new-personas-cell">
                      <input type="text" className="new-personas-input" value={newPersonasData.sexo} onChange={(e) => setNewPersonasData({ ...newPersonasData, sexo: e.target.value })} />
                    </td>
                    <td className="new-personas-cell">
                      <input type="text" className="new-personas-input" value={newPersonasData.correo} onChange={(e) => setNewPersonasData({ ...newPersonasData, correo: e.target.value })} />
                    </td>
                    <td className="new-personas-cell">
                      <input type="text" className="new-personas-input" value={newPersonasData.estado} onChange={(e) => setNewPersonasData({ ...newPersonasData, estado: e.target.value })} />
                    </td>
                    <td className="new-personas-cell">
                      <button onClick={handleSaveNewPersonas} className="new-personas-save-btn"><FaSave />Guardar</button>
                      <button onClick={() => setShowNewPersonasRow(false)} className="new-personas-cancel-btn"><MdCancel />Cancelar</button>
                    </td>
                  </tr>
                )}
                
                  {personasFiltradas.length > 0 ? (
                    personasFiltradas.map((persona) => (
                      <tr key={persona.cod_persona}>
                        <td>{persona.cod_persona}</td>
                        <td>
                          {editingPersonasId === persona.cod_persona ? (
                            <input className="input-editar" type="number" name="cod_tipo_persona" value={editedPersonasData.cod_tipo_persona || ''} onChange={(e) => setEditedPersonasData({ ...editedPersonasData, cod_tipo_persona: e.target.value })} />
                          ) : (
                            persona.cod_tipo_persona
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona? (
                            <input className="input-editar" type="text" name="dni" value={editedPersonasData.dni || ''} onChange={(e) =>setEditedPersonasData({ ...editedPersonasData, dni: e.target.value })}/>
                          ) : (
                            persona.dni
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona? (
                            <input className="input-editar" type="text" name="primer_nombre" value={editedPersonasData.primer_nombre || ''} onChange={(e) => setEditedPersonasData({ ...editedPersonasData, primer_nombre: e.target.value }) }/>
                          ) : (
                            persona.primer_nombre
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona? (
                            <input className="input-editar" type="text" name="apellido" value={editedPersonasData.apellido || ''} onChange={(e) => setEditedPersonasData({ ...editedPersonasData, apellido: e.target.value })}/>
                          ) : (
                            persona.apellido
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona? (
                            <input className="input-editar" type="date" name="fecha_nacimiento" value={editedPersonasData.fecha_nacimiento || ''} onChange={(e) => setEditedPersonasData({ ...editedPersonasData, fecha_nacimiento: e.target.value })} />
                          ) : (
                            persona.fecha_nacimiento
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona? (
                            <input className="input-editar" type="text" name="sexo" value={editedPersonasData.sexo || ''} onChange={(e) =>setEditedPersonasData({ ...editedPersonasData, sexo: e.target.value })}/>
                          ) : (
                            persona.sexo
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona? (
                            <input className="input-editar" type="text" name="correo" value={editedPersonasData.correo|| ''} onChange={(e) => setEditedPersonasData({ ...editedPersonasData, correo: e.target.value })} />
                          ) : (
                            persona.correo
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona? (
                            <input className="input-editar" type="text" name="estado" value={editedPersonasData.estado|| ''} onChange={(e) => setEditedPersonasData({ ...editedPersonasData, estado: e.target.value }) }/>
                          ) : (
                            persona.estado
                          )}
                        </td>
                        <td>
                          {editingPersonasId === persona.cod_persona? (
                            <>
                              <button onClick={handleSaveClick} className="new-personas-save-btn"><FaSave />Guardar</button>
                              <button className="new-personas-cancel-btn" onClick={() => setEditingPersonasId(null)}>{" "}<MdCancel />Cancelar{" "}</button>
                            </>
                          ) : (
                            <>
                            <button className="new-personas-edit-btn" onClick={() => handleEditClick(persona)}><FaEdit />Editar</button>
                            <button className="new-personas-delete-btn" onClick={() => handleDelete(persona.cod_persona)}><MdDelete />Eliminar</button>
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
            </div>
          </div>
        </div>
      </section>
    </div>
    </div>
  );
};

export default GestionPersonas;