import React, { useState } from "react";
import { FaBoxOpen, FaHourglassHalf } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { MdCheckCircle } from "react-icons/md";
import { FaArrowLeft } from "react-icons/fa";
import "./EstadoPaquete.css";


const paquetesIniciales = [
  { id: 1, nombre: "PAQUETE 01", pendiente: true, pagado: false },
  { id: 2, nombre: "PAQUETE 02", pendiente: false, pagado: true },
  { id: 3, nombre: "PAQUETE 03", pendiente: true, pagado: false },
];

const EstadoPaquete = () => {
  const [paquetes, setPaquetes] = useState(paquetesIniciales);
  const navigate = useNavigate();

  const toggleEstado = (id, campo) => {
    setPaquetes((prev) =>
      prev.map((p) => (p.id === id ? { ...p, [campo]: !p[campo] } : p))
    );
  };

  const handleRegresar = () => {
    navigate("/");
  };

  return (
    <div className="estado-paquete-container">
      <div className="contenido-tabla">
        <table className="tabla-paquetes">
          <thead>
            <tr>
              <th><FaBoxOpen /> PAQUETE</th>
              <th><FaHourglassHalf /> PENDIENTE</th>
              <th><MdCheckCircle /> PAGADO</th>
            </tr>
          </thead>
          <tbody>
            {paquetes.map((p) => (
              <tr key={p.id}>
                <td className="nombre-paquete">{p.nombre}</td>
                <td>
                  <label className="check-container">
                    <input
                      type="checkbox"
                      checked={p.pendiente}
                      onChange={() => toggleEstado(p.id, "pendiente")}
                    />
                    <span className="custom-check"></span>
                  </label>
                </td>
                <td>
                  <label className="check-container">
                    <input
                      type="checkbox"
                      checked={p.pagado}
                      onChange={() => toggleEstado(p.id, "pagado")}
                    />
                    <span className="custom-check"></span>
                  </label>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
  
        {/* Botones abajo */}
        <div className="boton-acciones">
          <button type="button" className="boton-guardar">
            Guardar Paquete
          </button>
          <button type="button" className="btn-regresar" onClick={handleRegresar}>
            <FaArrowLeft /> Regresar
          </button>
        </div>
      </div>
    </div>
  );  
};

export default EstadoPaquete;
