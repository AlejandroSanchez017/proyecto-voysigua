import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import LoginForm from './Frontend/Formularios/LoginForm';
import Home from './Frontend/Formularios/Home'; // Crea e importa el componente Home

function App() {
  return (
    <Router>
      <div>
        <Routes>
          {/* Configura la ruta principal y la de /home */}
          <Route path="/" element={<LoginForm />} />
          <Route path="/home" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

