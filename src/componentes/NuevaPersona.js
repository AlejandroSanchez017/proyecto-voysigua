import React, { useState } from "react";
import "./NuevaPersona.css";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";
import Swal from "sweetalert2";

const NuevaPersona = () => {
  const navigate = useNavigate();

  const [formulario, setFormulario] = useState({
    // Persona
    tipoPersona: "",
    dni: "",
    nombres: "",
    apellidos: "",
    fechaNacimiento: "",
    sexo: "",
    correo: "",
    estado: "A",
    // Teléfono
    tipoTelefono: "",
    numeroTelefono: "",
    exten: "",
    codigodearea: "",
    estadoTelefono: "A",
    // Dirección
    ciudad: "",
    tipoDireccion: "",
    direccion1: "",
    direccion2: "",
    direccion3: "",
    estadoDireccion: "A",
  });

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

      // 1. Insertar Persona
      const responsePersona = await fetch("https://proyecto-backend.onrender.com/personas/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cod_tipo_persona: formulario.tipoPersona,
          dni: formulario.dni,
          primer_nombre: formulario.nombres,
          apellido: formulario.apellidos,
          fecha_nacimiento: formulario.fechaNacimiento,
          sexo: formulario.sexo,
          correo: formulario.correo,
          estado: formulario.estado,
        }),
      });

      if (!responsePersona.ok) throw new Error("Error al guardar Persona");

      const nuevaPersona = await responsePersona.json();
      const codPersona = nuevaPersona.cod_persona; // ✔️

      // 2. Insertar Teléfono
      const responseTelefono = await fetch("https://proyecto-backend.onrender.com/telefonos/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cod_persona: codPersona,
          telefono_principal: formulario.numeroTelefono,
          exten: formulario.exten ? parseInt(formulario.exten) : null,
          codigo_area: formulario.codigodearea
            ? parseInt(formulario.codigodearea)
            : null,
          cod_tipo_telefono: parseInt(formulario.tipoTelefono),
          estado: formulario.estadoTelefono,
        }),
      });

      if (!responseTelefono.ok) throw new Error("Error al guardar Teléfono");

      // 3. Insertar Dirección
      const responseDireccion = await fetch(
        `https://proyecto-backend.onrender.com/direccion/?cod_persona=${codPersona}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            cod_ciudad: formulario.ciudad,
            cod_tipo_direccion: formulario.tipoDireccion,
            direccion1: formulario.direccion1,
            direccion2: formulario.direccion2,
            direccion3: formulario.direccion3,
            estado_direccion: formulario.estadoDireccion,
          }),
        }
      );

      if (!responseDireccion.ok) throw new Error("Error al guardar Dirección");

      Swal.close();

      Swal.fire({
        icon: "success",
        title: "¡Registro exitoso!",
        text: "Persona, teléfono y dirección guardados correctamente.",
        timer: 2000,
        showConfirmButton: false,
      });

      setTimeout(() => {
        navigate("/");
      }, 2000);
    } catch (error) {
      console.error(error);
      Swal.close();
      Swal.fire({
        icon: "error",
        title: "Error",
        text: error.message || "No se pudo guardar la persona.",
      });
    }
  };

  const handleRegresar = () => {
    navigate("/gestionpersonas");
  };

  return (
    <div className="nuevo-persona-container">
      <h1> </h1>
      <form onSubmit={handleSubmit} className="form-mandado">
        {/* 📦 Datos Generales */}
        <div className="seccion seccion-generales">
          <h3>Datos generales</h3>

          <div className="input-group-doble">
            <div>
              <label>Nombres:</label>
              <input
                type="text"
                name="nombres"
                value={formulario.nombres}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div>
              <label>Apellidos:</label>
              <input
                type="text"
                name="apellidos"
                value={formulario.apellidos}
                onChange={handleChange}
                className="form-control"
              />
            </div>
          </div>

          <div className="input-group-doble">
            <div>
              <label>Número de identidad:</label>
              <input
                type="text"
                name="dni"
                value={formulario.dni}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div>
              <label>Fecha de nacimiento:</label>
              <input
                type="date"
                name="fechaNacimiento"
                value={formulario.fechaNacimiento}
                onChange={handleChange}
                className="form-control"
              />
            </div>
          </div>

          <div className="input-group-doble">
            <div>
              <label>Sexo:</label>
              <select
                name="sexo"
                value={formulario.sexo}
                onChange={handleChange}
                className="form-control"
              >
                <option value="">Seleccione</option>
                <option value="M">Masculino</option>
                <option value="F">Femenino</option>
              </select>
            </div>
            <div>
              <label>Tipo de Persona:</label>
              <select
                name="tipoPersona"
                value={formulario.tipoPersona}
                onChange={handleChange}
                className="form-control"
              >
                <option value="">Seleccione</option>
                <option value="1">Administrador 1</option> {/* ID 1 */}
                <option value="2">Administrador 2</option> {/* ID 2 */}
                <option value="3">Usuario VoyNivel 1</option> {/* ID 3 */}
                <option value="4">Usuario VoyNivel 2</option> {/* ID 4 */}
                <option value="5">Usuario VoyNivel 3</option> {/* ID 5 */}
                <option value="6">Cliente</option> {/* ID 6 */}
                <option value="7">Motorista</option> {/* ID 7 */}
              </select>
            </div>
          </div>

          <div className="input-group-doble">
            <div>
              <label>Correo electrónico:</label>
              <input
                type="email"
                name="correo"
                value={formulario.correo}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div>
              <label>Estado:</label>
              <select
                name="estado"
                value={formulario.estado}
                onChange={handleChange}
                className="form-control"
              >
                <option value="A">Activo</option>
                <option value="I">Inactivo</option>
              </select>
            </div>
          </div>

          {/* 📦 Teléfonos */}
          <h3 style={{ marginTop: "30px" }}>Teléfonos</h3>

          <div className="input-group-doble">
            <div>
              <label>Tipo de Teléfono:</label>
              <select
                name="tipoTelefono"
                value={formulario.tipoTelefono}
                onChange={handleChange}
                className="form-control"
              >
                <option value="">Seleccione</option>
                <option value="1">Celular</option> {/* ID 1 */}
                <option value="2">Casa</option> {/* ID 2 */}
                <option value="3">Trabajo</option> {/* ID 3 */}
              </select>
            </div>
            <div>
              <label>Número:</label>
              <input
                type="text"
                name="numeroTelefono"
                value={formulario.numeroTelefono}
                onChange={handleChange}
                className="form-control"
              />
            </div>
          </div>

          <div className="input-group-doble">
            <div>
              <label>Extensión:</label>
              <input
                type="text"
                name="exten"
                value={formulario.exten}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div>
              <label>Código de Área:</label>
              <input
                type="text"
                name="codigodearea"
                value={formulario.codigodearea}
                onChange={handleChange}
                className="form-control"
              />
            </div>
          </div>
        </div>

        {/* 📦 Direcciones */}
        <div className="seccion seccion-direcciones">
          <h3>Direcciones</h3>

          <div className="input-group-doble">
            <div>
              <label>Ciudad:</label>
              <input
                type="text"
                name="ciudad"
                value={formulario.ciudad}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div>
              <label>Tipo de Direccion:</label>
              <select
                name="tipoDireccion"
                value={formulario.tipoDireccion}
                onChange={handleChange}
                className="form-control"
              >
                <option value="">Seleccione</option>
                <option value="1">Casa</option> {/* ID 1 */}
                <option value="2">Trabajo</option> {/* ID 2 */}
                <option value="3">Direccion Alternativa</option> {/* ID 3 */}
              </select>
            </div>
          </div>

          <div className="input-group-simple">
            <label>Dirección 1:</label>
            <textarea
              name="direccion1"
              value={formulario.direccion1}
              onChange={handleChange}
              className="form-control"
              rows="2"
            />
          </div>

          <div className="input-group-simple">
            <label>Dirección 2:</label>
            <textarea
              name="direccion2"
              value={formulario.direccion2}
              onChange={handleChange}
              className="form-control"
              rows="2"
            />
          </div>

          <div className="input-group-simple">
            <label>Dirección 3:</label>
            <textarea
              name="direccion3"
              value={formulario.direccion3}
              onChange={handleChange}
              className="form-control"
              rows="2"
            />
          </div>

          <div className="boton-acciones-direcciones">
            <button type="submit" className="boton-guardar">
              Guardar Persona
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

export default NuevaPersona;
