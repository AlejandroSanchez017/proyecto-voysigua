import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import GestionUsuarios from './componentes/GestionUsuarios';
import GestionPersonas from './componentes/GestionPersonas';
import GestionEmpleados from './componentes/GestionEmpleados';
import GestionTelefonos from './componentes/GestionTelefonos';
import LoginForm from './componentes/LoginForm';
import Adminlte from './componentes/adminlte';
import HomePrincipal from './componentes/HomePrincipal';
import MandadosDia from './componentes/Mandados';
import NuevoPaquete from './componentes/NuevoPaquete';
import EstadoPaquete from './componentes/EstadoPaquete';
import NuevoMandado from './componentes/NuevoMandado';
import NuevoUsuario from './componentes/NuevoUsuario'
import NuevaPersona from './componentes/NuevaPersona';
import NuevoEmpleado from './componentes/Nuevo Empleado';
import GestionDirecciones from './componentes/GestionDirecciones';
import Auditoria from './componentes/Auditoria';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!sessionStorage.getItem("token")
  );

  return (
    <Router>
      <div className="wrapper">
        <Routes>
          {/* Si está autenticado, muestra las rutas privadas */}
          {isAuthenticated ? (
            <>
              <Route
                path="/home"
                element={<HomePrincipal setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/mycomponent"
                element={<GestionUsuarios setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestionpersonas"
                element={<GestionPersonas setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestiontelefonos"
                element={<GestionTelefonos setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestiondirecciones"
                element={<GestionDirecciones setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/nuevopaquete"
                element={<NuevoPaquete setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/nuevousuario"
                element={<NuevoUsuario setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/estadopaquete"
                element={<EstadoPaquete setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/mandados"
                element={<MandadosDia setIsAuthenticated={setIsAuthenticated} />}
              /><Route
                path="/mandados"
                element={<MandadosDia setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/nuevomandados"
                element={<NuevoMandado setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestionempleados"
                element={<GestionEmpleados setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/auditoria"
                element={<Auditoria setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/home/admindashboard"
                element={<Adminlte setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/nuevapersona"
                element={<NuevaPersona setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/nuevoempleado"
                element={<NuevoEmpleado setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestionpersonas/admindashboard"
                element={<Adminlte setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestiontelefonos/admindashboard"
                element={<Adminlte setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestiondirecciones/admindashboard"
                element={<Adminlte setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestionempleados/admindashboard"
                element={<Adminlte setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route path="/" element={<Navigate to="/home" />} />
            </>
          ) : (
            <>
              <Route
                path="/"
                element={<LoginForm onLogin={setIsAuthenticated} />}
              />
              <Route path="*" element={<Navigate to="/" />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
