<<<<<<< HEAD
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import LoginForm from './Frontend/Formularios/LoginForm';
import Home from './Frontend/Formularios/Home'; // Crea e importa el componente Home
=======
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import MyComponent from './componentes/MyComponent';
import GestionPersonas from './componentes/GestionPersonas';
import GestionEmpleados from './componentes/GestionEmpleados';
import LoginForm from './componentes/LoginForm';
import Adminlte from './componentes/adminlte';
import HomePrincipal from './componentes/HomePrincipal';
>>>>>>> 6ffaf857b4c537e39578b73ede51210f016fb4ad




function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router>
<<<<<<< HEAD
      <div>
        <Routes>
          {/* Configura la ruta principal y la de /home */}
          <Route path="/" element={<LoginForm />} />
          <Route path="/home" element={<Home />} />
=======
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
>>>>>>> 6ffaf857b4c537e39578b73ede51210f016fb4ad
        </Routes>
      </div>
    </Router>
  );
}

export default App;

<<<<<<< HEAD
=======

>>>>>>> 6ffaf857b4c537e39578b73ede51210f016fb4ad
