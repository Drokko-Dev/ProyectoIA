import { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [mensaje, setMensaje] = useState("Cargando...");

  useEffect(() => {
    // Llamada al backend de Docker
    fetch("http://localhost:8000/")
      .then((res) => res.json())
      .then((data) => setMensaje(data.message)) // Suponiendo que tu JSON tiene "message"
      .catch((err) => setMensaje("Error conectando al backend"));
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Mi Proyecto Full Stack</h1>
      <div>
        <p>
          Respuesta del Backend: <strong>{mensaje}</strong>
        </p>
      </div>
    </div>
  );
}

export default App;
