import { useState, useEffect } from "react";

function Voice_IA({ texto, onTextoCambiado }) {
  const [audioUrl, setAudioUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch(
        `${import.meta.env.VITE_URL_BACKEND}/api/generate-voice`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          // Enviamos el texto editado y validado por el usuario
          body: JSON.stringify({ prompt: texto }),
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

export default Voice_IA;
