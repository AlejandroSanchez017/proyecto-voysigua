import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import MyComponent from './componentes/MyComponent';
import GestionPersonas from './componentes/GestionPersonas';
import GestionEmpleados from './componentes/GestionEmpleados';
import LoginForm from './componentes/LoginForm';
import Adminlte from './componentes/adminlte';
import HomePrincipal from './componentes/HomePrincipal';
import MandadosDia from './componentes/Mandados';
import NuevoPaquete from './componentes/NuevoPaquete';
import EstadoPaquete from './componentes/EstadoPaquete';
import NuevoMandado from './componentes/NuevoMandado';
import NuevoUsuario from './componentes/NuevoUsuario'

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
                element={<MyComponent setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestionpersonas"
                element={<GestionPersonas setIsAuthenticated={setIsAuthenticated} />}
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
                path="/home/admindashboard"
                element={<Adminlte setIsAuthenticated={setIsAuthenticated} />}
              />
              <Route
                path="/gestionpersonas/admindashboard"
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
