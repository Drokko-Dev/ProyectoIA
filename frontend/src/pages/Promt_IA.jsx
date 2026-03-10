import { useState, useEffect } from "react";

function Promt_IA() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch(
        `${import.meta.env.VITE_URL_BACKEND}/api/generate-script-voice`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt: input }),
        },
      );

      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      setResponse("Error al conectar con la IA.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitTest = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // 1. Usamos la URL exacta donde el backend está sirviendo el archivo
      const urlDelArchivo = `${import.meta.env.VITE_URL_BACKEND}/archivos/texts/gen_20260310_025631.txt`;

      // 2. Hacemos la petición
      const res = await fetch(urlDelArchivo);

      // 3. OJO: Usamos .text() en lugar de .json() porque es un archivo de texto plano
      const texto = await res.text();

      // 4. Lo guardamos en el estado para mostrarlo en pantalla
      setResponse(texto);
    } catch (error) {
      console.error("Error leyendo el archivo:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        padding: "40px",
        maxWidth: "600px",
        margin: "auto",
        fontFamily: "sans-serif",
        borderBottom: "1px solid #ddd",
      }}
    >
      <h1>1. 🤖 Mi Asistente IA</h1>

      <form onSubmit={handleSubmitTest}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Descripción Técnica:"
          style={{
            width: "100%",
            height: "100px",
            padding: "10px",
            marginBottom: "10px",
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{ padding: "10px 20px", cursor: "pointer" }}
        >
          {loading ? "Pensando..." : "Enviar a la IA"}
        </button>
      </form>

      {response && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            backgroundColor: "#f4f4f4",
            borderRadius: "8px",
            color: "#333",
          }}
        >
          <strong>Respuesta:</strong>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default Promt_IA;
