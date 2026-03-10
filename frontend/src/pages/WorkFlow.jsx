import { useState } from "react";
import Promt_IA from "../components/Promt_IA";
import VoiceIA from "../components/Voice_IA";

function WorkFlow() {
  // Este estado es el puente entre ambos componentes
  const [textoGenerado, setTextoGenerado] = useState("");

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
      <h1>🦷 Creador de Contenido</h1>

      {/* Paso 1: Generar el texto */}
      <Promt_IA onTextoGenerado={(texto) => setTextoGenerado(texto)} />

      {/* Paso 2: Solo mostramos VoiceIA si ya hay texto generado */}
      {textoGenerado && (
        <div
          style={{
            marginTop: "30px",
            borderTop: "2px solid #ccc",
            paddingTop: "20px",
          }}
        >
          <VoiceIA texto={textoGenerado} onTextoCambiado={setTextoGenerado} />
        </div>
      )}
    </div>
  );
}

export default WorkFlow;
