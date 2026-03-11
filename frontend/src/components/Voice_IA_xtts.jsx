import { useState, useEffect } from "react";

function Voice_IA_xtts({ texto, onTextoCambiado }) {
  const [audioUrl, setAudioUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [vozSeleccionada, setVozSeleccionada] = useState("voz_jimmy.wav");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch(
        `${import.meta.env.VITE_URL_BACKEND}/api/generate-voice-xtts`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          // 2. NUEVO BODY: Enviamos el texto y la voz que eligió el usuario
          body: JSON.stringify({
            prompt: texto,
            voz: vozSeleccionada,
          }),
        },
      );

      const data = await res.json();
      // Guardamos directamente la URL del audio que viene del backend
      setAudioUrl(data.response.audio_url);
    } catch (error) {
      console.error("Error al conectar con la IA:", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div
      style={{
        padding: "40px",
        maxWidth: "750px",
        margin: "auto",
        fontFamily: "sans-serif",
      }}
    >
      <h1>2. 🎙️ Generador de Voz con IA</h1>

      <form onSubmit={handleSubmit}>
        <textarea
          value={texto} // El texto viene controlado desde el Padre
          onChange={(e) => onTextoCambiado(e.target.value)} // Si editan el texto, el Padre se entera
          placeholder="El guion generado aparecerá aquí para que lo revises..."
          style={{
            width: "100%",
            height: "100px",
            padding: "10px",
            marginBottom: "10px",
          }}
        />
        <div style={{ marginBottom: "20px" }}>
          <label style={{ marginRight: "10px", fontWeight: "bold" }}>
            Elige tu Locutor:
          </label>
          <select
            value={vozSeleccionada}
            onChange={(e) => setVozSeleccionada(e.target.value)}
            style={{
              padding: "8px",
              borderRadius: "5px",
              border: "1px solid #ccc",
            }}
          >
            <option value="referencia.wav">Voz Principal (Masculina)</option>
            <option value="voz_mhaivy.wav">Doctora (Femenina)</option>
            <option value="voz_jaime.wav">Mi Voz</option>
          </select>
        </div>
        <button
          type="submit"
          // Deshabilitamos el botón si está cargando o si no hay texto
          disabled={loading || !texto.trim()}
          style={{ padding: "10px 20px", cursor: "pointer" }}
        >
          {loading ? "Grabando en el estudio..." : "Generar Audio"}
        </button>
      </form>

      {/* Renderizamos el reproductor nativo del navegador */}
      {audioUrl && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            backgroundColor: "#f4f4f4",
            borderRadius: "8px",
            color: "#333",
          }}
        >
          <strong>¡Audio Listo! 🎧</strong>
          <div style={{ marginTop: "15px" }}>
            <audio controls src={audioUrl} style={{ width: "100%" }}>
              Tu navegador no soporta el elemento de audio.
            </audio>
          </div>
        </div>
      )}
    </div>
  );
}

export default Voice_IA_xtts;
