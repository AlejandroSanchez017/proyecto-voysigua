import React, { useState } from "react";
import { FaPlus, FaEdit } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import Swal from "sweetalert2";
import Adminlte from "./adminlte";
import "./Mandados.css"; // Puedes adaptar esto a tu estructura

const mandadosEjemplo = [
  {
    id: 1,
    cliente: "Jackelyn Reyes",
    tipo: "Restaurante",
    estado: "Disponible",
    motorista: "Luis Villatoro",
  },
  {
    id: 2,
    cliente: "Nicoll Ordoñez",
    tipo: "Farmacia",
    estado: "Disponible",
    motorista: "Carlos Baquedano",
  },
  {
    id: 3,
    cliente: "Dennis Carrillo",
    tipo: "Banco",
    estado: "Ocupado",
    motorista: "Felipe Fuentes",
  },
];

const MandadosDia = () => {
  const [mandados, setMandados] = useState(mandadosEjemplo);
  const [cantidad, setCantidad] = useState(3);
  const [busqueda, setBusqueda] = useState("");

  const handleDelete = (id) => {
    Swal.fire({
      title: "¿Estás seguro?",
      text: "Este mandado será eliminado",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#aaa",
      confirmButtonText: "Sí, eliminar",
    }).then((result) => {
      if (result.isConfirmed) {
        setMandados((prev) => prev.filter((m) => m.id !== id));
        Swal.fire("Eliminado", "El mandado fue eliminado", "success");
      }
    });
  };

  const mandadosFiltrados = mandados
    .filter((m) => m.cliente.toLowerCase().includes(busqueda.toLowerCase()))
    .slice(0, cantidad);

  return (
    <div>
      <Adminlte />
      <div className="content-wrapper">
        <h1> </h1>
        <section className="content">
            <div className="container-fluid">
                 {/* Tarjetas resumen */}
        <div className="resumen-cards">
          <div className="card card-yellow">
            <p>
              <strong>Mandados Realizados</strong>
            </p>
            <span>15</span>
          </div>
          <div className="card card-green">
            <p>
              <strong>Mandados en Proceso</strong>
            </p>
            <span>7</span>
          </div>
          <div className="card card-blue">
            <p>
              <strong>Motoristas Disponibles</strong>
            </p>
            <span>10</span>
          </div>
        </div>

        {/* Controles */}
        <div className="filtros">
          <label>
            Mostrar&nbsp;
            <select
              value={cantidad}
              onChange={(e) => setCantidad(Number(e.target.value))}
            >
              <option value="3">3</option>
              <option value="10">10</option>
              <option value="50">50</option>
            </select>
          </label>
          <input
            type="text"
            placeholder="Buscar..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
        </div>

        {/* Tabla */}
        <h1 className="card-title"><center> Mandados del dia</center></h1>
        <table className="table table-bordered table-striped">
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Tipo de Mandado</th>
              <th>Estado del Mandado</th>
              <th>Motorista</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {mandadosFiltrados.map((mandado) => (
              <tr key={mandado.id}>
                <td>{mandado.cliente}</td>
                <td>{mandado.tipo}</td>
                <td>{mandado.estado}</td>
                <td>{mandado.motorista}</td>
                <td>
                  <button className="btn-accion">
                    <FaPlus />
                  </button>
                  <button
                    className="btn-accion"
                    onClick={() => handleDelete(mandado.id)}
                  >
                    <MdDelete />
                  </button>
                  <button className="btn-accion">
                    <FaEdit />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
            </div>
        </section>
       
      </div>
    </div>
  );
};

export default MandadosDia;
