import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

const Dashboard = () => {
    const salesChartRef = useRef(null);
    const pieChartRef = useRef(null);

    useEffect(() => {
        console.log("DOM completamente cargado, ejecutando dashboard.js");

        // Configuración del gráfico de ventas
        if (salesChartRef.current) {
            console.log("Canvas de ventas encontrado");
            const ctx = salesChartRef.current.getContext("2d");

            new Chart(ctx, {
                type: "line",
                data: {
                    labels: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio"],
                    datasets: [
                        {
                            label: "Digital Goods",
                            backgroundColor: "rgba(60,141,188,0.9)",
                            borderColor: "rgba(60,141,188,0.8)",
                            data: [28, 48, 40, 19, 86, 27, 90]
                        },
                        {
                            label: "Electronics",
                            backgroundColor: "rgba(210, 214, 222, 1)",
                            borderColor: "rgba(210, 214, 222, 1)",
                            data: [65, 59, 80, 81, 56, 55, 40]
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false } },
                        y: { grid: { display: false } }
                    }
                }
            });
        } else {
            console.error("Canvas de ventas no encontrado, verifica que esté en el HTML.");
        }

        // Configuración del gráfico de ventas por categoría
        if (pieChartRef.current) {
            console.log("Canvas de gráfico circular encontrado");
            const ctx = pieChartRef.current.getContext("2d");

            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: ["Ventas en tienda", "Ventas online", "Ventas por correo"],
                    datasets: [
                        {
                            data: [30, 12, 20],
                            backgroundColor: ["#f56954", "#00a65a", "#f39c12"]
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        } else {
            console.error(" Canvas de gráfico circular no encontrado.");
        }
    }, []);

    return (
        <div>
            <h2 className="text-center">Dashboard</h2>
            <div style={{ display: "flex", justifyContent: "center", gap: "20px", flexWrap: "wrap" }}>
                <canvas ref={salesChartRef} id="revenue-chart-canvas" width="400" height="200"></canvas>
                <canvas ref={pieChartRef} id="sales-chart-canvas" width="200" height="200"></canvas>
            </div>
        </div>
    );
};

export default Dashboard;
