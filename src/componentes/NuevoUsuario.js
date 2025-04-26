import React, { useState } from "react";
import Swal from "sweetalert2";
import "./NuevoUsuario.css";
import Adminlte from "./adminlte";

const NuevoUsuario = () => {
  const [formData, setFormData] = useState({
    cod_persona: "",
    nombre: "",
    username: "",
    password: "",
    estado: 1,
    primera_vez: false,
    fecha_vencimiento: "",
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const parsedData = {
        ...formData,
        cod_persona: parseInt(formData.cod_persona),
      };

      const response = await fetch("http://localhost:8000/usuarios/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(parsedData),
      });

      if (!response.ok) {
        const errorDetails = await response.text();
        throw new Error(errorDetails || "Error al crear el usuario");
      }

      Swal.fire({
        icon: "success",
        title: "Usuario creado",
        text: "El usuario ha sido creado correctamente.",
      });

      setFormData({
        cod_persona: "",
        nombre: "",
        username: "",
        password: "",
        estado: 1,
        primera_vez: false,
        fecha_vencimiento: "",
      });
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: error.message,
      });
    }
  };

  return (
    <div>
      <Adminlte />
      <div className="Content-Wrapper">
        <h1> </h1>
        <section className="container-fluid">
          <div className="usuario-form-container">
            <form onSubmit={handleSubmit} className="form-usuario">
              <fieldset>
                <legend>Agregar Usuario</legend>

                <label>Código de Persona:</label>
                <input
                  name="cod_persona"
                  type="number"
                  value={formData.cod_persona}
                  onChange={handleChange}
                />

                <label>Nombre:</label>
                <input
                  name="nombre"
                  type="text"
                  value={formData.nombre}
                  onChange={handleChange}
                />

                <label>Nombre de Usuario:</label>
                <input
                  name="username"
                  type="text"
                  value={formData.username}
                  onChange={handleChange}
                />

                <label>Contraseña:</label>
                <input
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                />

                <label>Estado:</label>
                <select
                  name="estado"
                  value={formData.estado}
                  onChange={handleChange}
                >
                  <option value={1}>Activo</option>
                  <option value={0}>Inactivo</option>
                </select>

                <label>Primera vez:</label>
                <input
                  name="primera_vez"
                  type="checkbox"
                  checked={formData.primera_vez}
                  onChange={handleChange}
                />

                <label>Fecha de vencimiento:</label>
                <input
                  name="fecha_vencimiento"
                  type="date"
                  value={formData.fecha_vencimiento}
                  onChange={handleChange}
                />

                <button className="boton-guardar-usuario" type="submit">
                  Guardar Usuario
                </button>
              </fieldset>
            </form>
          </div>
        </section>
      </div>
    </div>
  );
};

export default NuevoUsuario;
