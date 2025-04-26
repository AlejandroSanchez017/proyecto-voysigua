import React, { useState } from "react";
import { FaSearch } from "react-icons/fa";
import "./NuevoMandado.css";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";

const NuevoMandado = () => {
const navigate = useNavigate();
  const [form, setForm] = useState({
    cliente: "",
    tipo: "Restaurante",
    descripcion: "",
    detalles: "",
    estado: "Sin asignar",
    tipo_pago: "Efectivo",
    costo_estandar: 100,
    costo_extra: 0,
    total: 100,
    motorista: "",
    hora_asignacion: "00:00:00",
    hora_finalizacion: "00:00:00",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    let updated = { ...form, [name]: value };

    if (name === "costo_extra") {
      updated.total = parseFloat(updated.costo_estandar) + parseFloat(value);
    }

    setForm(updated);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Mandado guardado");
  };

  const handleRegresar = () => {
    navigate("/");
  };

  return (
    <div className="nuevo-mandado-container">
      <form onSubmit={handleSubmit} className="form-mandado">
        <div className="seccion seccion-generales">
          <h3>Datos generales</h3>
          <label>Cliente:</label>
          <div className="input-group">
            <input
              name="cliente"
              value={form.cliente}
              onChange={handleChange}
            />
            <button type="button" className="buscar-btn">
              <FaSearch />
            </button>
          </div>

          <label>Tipo de mandado:</label>
          <select name="tipo" value={form.tipo} onChange={handleChange}>
            <option>Restaurante</option>
            <option>Farmacia</option>
            <option>Banco</option>
          </select>

          <label>Descripción:</label>
          <textarea
            name="descripcion"
            value={form.descripcion}
            onChange={handleChange}
          />

          <label>Detalles:</label>
          <textarea
            name="detalles"
            value={form.detalles}
            onChange={handleChange}
          />

          <label>Estado del mandado:</label>
          <input value={form.estado} disabled />
          <div className="boton-acciones">
          <button type="button" className="boton-guardar">
            Guardar Paquete
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

        <div className="seccion seccion-costos">
          <h3>Costos</h3>
          <label>Tipo de pago:</label>
          <select
            name="tipo_pago"
            value={form.tipo_pago}
            onChange={handleChange}
          >
            <option>Efectivo</option>
            <option>Tarjeta</option>
          </select>

          <label>Costo estándar:</label>
          <input value={`L. ${form.costo_estandar.toFixed(2)}`} disabled />

          <label>Costo extra:</label>
          <input
            type="number"
            name="costo_extra"
            value={form.costo_extra}
            onChange={handleChange}
          />

          <label>Total Costo:</label>
          <input value={`L. ${form.total.toFixed(2)}`} disabled />
        </div>

        <div className="seccion seccion-motorista">
          <h3>Motorista</h3>
          <label>Asignar a:</label>
          <div className="input-group">
            <input
              name="motorista"
              value={form.motorista}
              onChange={handleChange}
            />
            <button type="button" className="buscar-btn">
              <FaSearch />
            </button>
          </div>

          <label>Hora de asignación:</label>
          <input value={form.hora_asignacion} disabled />

          <label>Hora de finalización:</label>
          <input value={form.hora_finalizacion} disabled />
        </div>
      </form>
    </div>
  );
};

export default NuevoMandado;
