import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import { FaArrowLeft } from "react-icons/fa";
import "./NuevoPaquete.css";

const NuevoPaquete = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    remitente: "",
    destinatario: "",
    tamano: "Grande",
    descripcion: "",
    valor_paquete: 0,
    costo_envio: 0,
    costo_adicional: 0,
    foto: null,
    nombre_ruta: "",
    numero_ruta: "",
    destino: "",
    procedencia: "",
    valor_ruta: 0,
  });

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === "file") {
      setForm({ ...form, [name]: files[0] });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.remitente || !form.destinatario) {
      return Swal.fire(
        "Campos obligatorios",
        "Completa remitente y destinatario",
        "warning"
      );
    }

    // Aquí se haría la petición al backend
    Swal.fire("¡Éxito!", "Paquete registrado correctamente", "success");

    setForm({
      remitente: "",
      destinatario: "",
      tamano: "Grande",
      descripcion: "",
      valor_paquete: 0,
      costo_envio: 0,
      costo_adicional: 0,
      foto: null,
      nombre_ruta: "",
      numero_ruta: "",
      destino: "",
      procedencia: "",
      valor_ruta: 0,
    });
  };

  const handleRegresar = () => {
    navigate("/");
  };

  return (
    <div className="nuevo-paquete-container">
      <form onSubmit={handleSubmit} className="paquete-form">
        <fieldset className="grupo">
          <legend>Datos generales</legend>
          <div className="col">
            <label>Remitente</label>
            <input
              name="remitente"
              value={form.remitente}
              onChange={handleChange}
            />

            <label>Destinatario</label>
            <input
              name="destinatario"
              value={form.destinatario}
              onChange={handleChange}
            />

            <label>Tamaño</label>
            <select name="tamano" value={form.tamano} onChange={handleChange}>
              <option>Pequeño</option>
              <option>Mediano</option>
              <option>Grande</option>
            </select>

            <label>Descripción</label>
            <textarea
              name="descripcion"
              value={form.descripcion}
              onChange={handleChange}
            />
          </div>

          <div className="col">
            <label>Foto paquete</label>
            <input
              type="file"
              name="foto"
              accept="image/*"
              onChange={handleChange}
            />

            <label>Valor paquete</label>
            <input
              type="number"
              name="valor_paquete"
              value={form.valor_paquete}
              onChange={handleChange}
            />

            <label>Costo envío</label>
            <input
              type="number"
              name="costo_envio"
              value={form.costo_envio}
              onChange={handleChange}
            />

            <label>Costo adicional</label>
            <input
              type="number"
              name="costo_adicional"
              value={form.costo_adicional}
              onChange={handleChange}
            />
          </div>
        </fieldset>

        <fieldset className="grupo">
          <legend>Ruta</legend>
          <div className="col">
            <label>Nombre Ruta</label>
            <input
              name="nombre_ruta"
              value={form.nombre_ruta}
              onChange={handleChange}
            />

            <label>Numero Ruta</label>
            <input
              name="numero_ruta"
              value={form.numero_ruta}
              onChange={handleChange}
            />

            <label>Destino</label>
            <input
              name="destino"
              value={form.destino}
              onChange={handleChange}
            />
          </div>

          <div className="col">
            <label>Procedencia</label>
            <input
              name="procedencia"
              value={form.procedencia}
              onChange={handleChange}
            />

            <label>Valor ruta</label>
            <input
              type="number"
              name="valor_ruta"
              value={form.valor_ruta}
              onChange={handleChange}
            />
          </div>
        </fieldset>
        <div className="boton-acciones">
          <button type="button" className="boton-guardar">Guardar Paquete</button>
          <button type="button" className="btn-regresar" onClick={handleRegresar}> <FaArrowLeft /> Regresar </button>
        </div>
      </form>
    </div>
  );
};

export default NuevoPaquete;
