import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import { FaArrowLeft } from "react-icons/fa";
import "./NuevoUsuario.css";

const NuevoUsuario = () => {
  const navigate = useNavigate();

  const [personas, setPersonas] = useState([]);
  const [formData, setFormData] = useState({
    cod_persona: "",
    nombre: "",
    username: "",
    password: "",
    estado: 1,
    primera_vez: false,
    fecha_vencimiento: "",
  });

  useEffect(() => {
    const fetchPersonas = async () => {
      try {
        const response = await fetch("http://localhost:8000/personas/");
        const data = await response.json();
        setPersonas(data);
      } catch (error) {
        console.error("Error al cargar personas:", error);
        Swal.fire({
          icon: "error",
          title: "Error al cargar personas",
          text: "Hubo un problema al cargar las personas. Intenta más tarde.",
        });
      }
    };

    fetchPersonas();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (name === "cod_persona") {
      const personaSeleccionada = personas.find(
        (p) => p.cod_persona === parseInt(value)
      );
      setFormData((prev) => ({
        ...prev,
        cod_persona: value,
        nombre: personaSeleccionada
          ? `${personaSeleccionada.primer_nombre} ${personaSeleccionada.apellido}`
          : "",
      }));
    } else if (type === "checkbox") {
      setFormData((prev) => ({
        ...prev,
        [name]: checked,
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      Swal.fire({
        title: "Guardando datos...",
        allowOutsideClick: false,
        didOpen: () => {
          Swal.showLoading();
        },
      });

      const response = await fetch("http://localhost:8000/usuarios/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...formData,
          cod_persona: parseInt(formData.cod_persona),
        }),
      });

      if (!response.ok) {
        if (response.status === 422) {
          throw new Error("Por favor completa todos los campos obligatorios.");
        }
        const errorDetails = await response.text();
        throw new Error(errorDetails || "Error al crear el usuario.");
      }

      Swal.close();

      Swal.fire({
        icon: "success",
        title: "¡Usuario creado exitosamente!",
        text: "El usuario ha sido registrado correctamente.",
        timer: 2000,
        showConfirmButton: false,
      });

      setTimeout(() => {
        navigate("/"); // 🚀 Redirige a la página principal después de 2s
      }, 2000);

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
      Swal.close();
      Swal.fire({
        icon: "error",
        title: "Error",
        text: error.message || "No se pudo guardar el usuario.",
      });
    }
  };

  const handleRegresar = () => {
    navigate("/mycomponent");
  };

  return (
    <div>
      <div className="content-wrapper">
        <h1> </h1>
        <section className="container-fluid">
          <div className="usuario-form-container">
            <form onSubmit={handleSubmit} className="form-usuario">
              <fieldset>
                <legend>Agregar Usuario</legend>

                <label>Código de Persona:</label>
                <select
                  name="cod_persona"
                  value={formData.cod_persona}
                  onChange={handleChange}
                  className="form-control"
                >
                  <option value="">Seleccione una persona</option>
                  {personas.map((persona) => (
                    <option
                      key={persona.cod_persona}
                      value={persona.cod_persona}
                    >
                      {persona.cod_persona} - {persona.primer_nombre}{" "}
                      {persona.apellido}
                    </option>
                  ))}
                </select>

                <label>Nombre:</label>
                <input
                  name="nombre"
                  type="text"
                  value={formData.nombre}
                  onChange={handleChange}
                  className="form-control"
                  readOnly
                />

                <label>Nombre de Usuario:</label>
                <input
                  name="username"
                  type="text"
                  value={formData.username}
                  onChange={handleChange}
                  className="form-control"
                />

                <label>Contraseña:</label>
                <input
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="form-control"
                />

                <label>Estado:</label>
                <select
                  name="estado"
                  value={formData.estado}
                  onChange={handleChange}
                  className="form-control"
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
                  className="form-control"
                />

                <div className="botones-acciones">
                  <button type="submit" className="boton-guardar">
                    Guardar Usuario
                  </button>
                  <button
                    type="button"
                    className="btn-regresar"
                    onClick={handleRegresar}
                  >
                    <FaArrowLeft /> Regresar
                  </button>
                </div>
              </fieldset>
            </form>
          </div>
        </section>
      </div>
    </div>
  );
};

export default NuevoUsuario;
