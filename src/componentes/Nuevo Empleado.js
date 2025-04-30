import React, { useState, useEffect } from "react";
import "./NuevoEmpleado.css";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";
import Swal from "sweetalert2";

const NuevoEmpleado = () => {
  const navigate = useNavigate();

  const [formulario, setFormulario] = useState({
    cod_persona: "",
    cod_tipo_empleado: "",
    cod_area: "",
    cod_tipo_contrato: "",
    fecha_contratacion: "",
    salario: "",
    estado_empleado: "A",
  });

  const [personas, setPersonas] = useState([]); //  inicia vacío como array

  useEffect(() => {
    const fetchPersonas = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/personas/`);
        const data = await response.json();

        if (Array.isArray(data)) {
          //  aseguramos que sea un array
          setPersonas(data);
        } else {
          setPersonas([]); // si no es array, lo dejamos vacío para evitar errores
          console.error("Respuesta inesperada en personas:", data);
        }
      } catch (error) {
        console.error("Error al cargar personas:", error);
        setPersonas([]); // en caso de error también
      }
    };

    fetchPersonas();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormulario({ ...formulario, [name]: value });
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

      const response = await fetch(`${process.env.REACT_APP_API_URL}/empleados/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formulario,
          cod_persona: parseInt(formulario.cod_persona),
          cod_tipo_empleado: parseInt(formulario.cod_tipo_empleado),
          cod_area: parseInt(formulario.cod_area),
          cod_tipo_contrato: parseInt(formulario.cod_tipo_contrato),
          salario: parseFloat(formulario.salario),
        }),
      });

      if (!response.ok) {
        if (response.status === 422) {
          throw new Error("Por favor completa todos los campos obligatorios.");
        }
        const errorDetails = await response.text();
        throw new Error(errorDetails || "Error al crear el empleado.");
      }

      Swal.close();

      Swal.fire({
        icon: "success",
        title: "¡Registro exitoso!",
        text: "Empleado guardado correctamente.",
        timer: 2000,
        showConfirmButton: false,
      });

      setTimeout(() => {
        navigate("/"); // 🚀 Regresar a página principal después de 2 segundos
      }, 2000);
    } catch (error) {
      console.error(error);
      Swal.close();
      Swal.fire({
        icon: "error",
        title: "Error",
        text: error.message || "No se pudo guardar el empleado.",
      });
    }
  };

  const handleRegresar = () => {
    navigate("/gestionempleados");
  };

  return (
    <div className="nuevo-empleado-container">
      <h1> </h1>
      <form onSubmit={handleSubmit} className="form-empleado">
        <div className="seccion seccion-empleado">
          <h3>Datos del Empleado</h3>

          <div className="input-group-doble">
            <div>
              <label>Código de Persona:</label>
              <select
                name="cod_persona"
                value={formulario.cod_persona}
                onChange={handleChange}
                className="form-control"
              >
                <option value="">Seleccione una persona</option>
                {personas.map((persona) => (
                  <option key={persona.cod_persona} value={persona.cod_persona}>
                    {persona.cod_persona} - {persona.primer_nombre}{" "}
                    {persona.apellido}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label>Tipo de Empleado:</label>
              <select
                name="cod_tipo_empleado"
                value={formulario.cod_tipo_empleado}
                onChange={handleChange}
                className="form-control"
              >
                <option value="">Seleccione</option>
                <option value="1">Administrativo</option>
                <option value="2">Operativo</option>
                <option value="3">Gerencial</option>
              </select>
            </div>
          </div>

          <div className="input-group-doble">
            <div>
              <label>Área de Trabajo:</label>
              <select
                name="cod_area"
                value={formulario.cod_area}
                onChange={handleChange}
                className="form-control"
              >
                <option value="">Seleccione</option>
                <option value="1">Administrativo</option>
                <option value="2">Mandados</option>
                <option value="3">Paqueteria</option>
              </select>
            </div>
            <div>
              <label>Tipo de Contrato:</label>
              <select
                name="cod_tipo_contrato"
                value={formulario.cod_tipo_contrato}
                onChange={handleChange}
                className="form-control"
              >
                <option value="">Seleccione</option>
                <option value="1">Indefinido</option>
                <option value="2">Temporal</option>
                <option value="3">Permanente</option>
              </select>
            </div>
          </div>

          <div className="input-group-doble">
            <div>
              <label>Fecha de Contratación:</label>
              <input
                type="date"
                name="fecha_contratacion"
                value={formulario.fecha_contratacion}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div>
              <label>Salario:</label>
              <input
                type="number"
                name="salario"
                value={formulario.salario}
                onChange={handleChange}
                className="form-control"
              />
            </div>
          </div>

          <div className="input-group-doble">
            <div>
              <label>Estado del Empleado:</label>
              <select
                name="estado_empleado"
                value={formulario.estado_empleado}
                onChange={handleChange}
                className="form-control"
              >
                <option value="A">Activo</option>
                <option value="I">Inactivo</option>
              </select>
            </div>
          </div>

          <div className="boton-acciones-empleado">
            <button type="submit" className="boton-guardar">
              Guardar Empleado
            </button>
            <button
              type="button"
              className="btn-regresar"
              onClick={handleRegresar}
            >
              <FaArrowLeft /> Regresar
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default NuevoEmpleado;
