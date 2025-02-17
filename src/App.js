import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import MyComponent from './componentes/MyComponent';
import GestionPersonas from './componentes/GestionPersonas';
import GestionEmpleados from './componentes/GestionEmpleados';
import LoginForm from './componentes/LoginForm';
import Adminlte from './componentes/adminlte';
import HomePrincipal from './componentes/HomePrincipal';




function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router>
      <div className="wrapper">
        <Routes>
          {/* Si está autenticado, muestra las rutas privadas */}
          {isAuthenticated ? (
            <>
              <Route path="/home" element={<HomePrincipal />}>
                <Route path="/home/admindashboard" element={<Adminlte />} />
              </Route>
              <Route path="/" element={<Navigate to="/home" />} /> {/* Redirige a home si ya está autenticado */}
              <Route path="/mycomponent" element={<MyComponent />} />
              <Route path="/gestionpersonas" element={<GestionPersonas />}>
                <Route path="/gestionpersonas/admindashboard" element={<Adminlte />} />
              </Route>
              <Route path="/gestionempleados" element={<GestionEmpleados />}>
                <Route path="/gestionempleados/admindashboard" element={<Adminlte />} />
              </Route>
              
            </>
          ) : (
            <>
              {/* Si no está autenticado, muestra la pantalla de login */}
              <Route path="/" element={<LoginForm onLogin={setIsAuthenticated} />} />
              <Route path="*" element={<Navigate to="/" />} /> {/* Redirige a login si no está autenticado */}
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;


