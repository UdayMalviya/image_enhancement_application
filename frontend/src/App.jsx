import { ImageUp, Loader2, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

const methods = ["sharpness", "contrast", "brightness"];

export default function App() {
  const [file, setFile] = useState(null);
  const [factor, setFactor] = useState(1.5);
  const [method, setMethod] = useState("sharpness");
  const [previewUrl, setPreviewUrl] = useState("");
  const [resultUrl, setResultUrl] = useState("");
  const [status, setStatus] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!file) {
      setPreviewUrl("");
      return;
    }

    const nextPreviewUrl = URL.createObjectURL(file);
    setPreviewUrl(nextPreviewUrl);

    return () => URL.revokeObjectURL(nextPreviewUrl);
  }, [file]);

  useEffect(() => {
    return () => {
      if (resultUrl) URL.revokeObjectURL(resultUrl);
    };
  }, [resultUrl]);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      setStatus("Choose an image first.");
      return;
    }

    setIsLoading(true);
    setStatus("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("factor", String(factor));
    formData.append("method", method);

    try {
      const response = await fetch(`${API_URL}/enhance/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => null);
        throw new Error(error?.detail ?? "Enhancement failed.");
      }

      const blob = await response.blob();
      if (resultUrl) URL.revokeObjectURL(resultUrl);
      setResultUrl(URL.createObjectURL(blob));
      setStatus("Done.");
    } catch (error) {
      setStatus(error.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <form className="controls" onSubmit={handleSubmit}>
          <div>
            <p className="eyebrow">FastAPI + React</p>
            <h1>Image Enhancement</h1>
          </div>

          <label className="dropzone">
            <ImageUp aria-hidden="true" />
            <span>{file ? file.name : "Choose image"}</span>
            <input
              accept="image/*"
              type="file"
              onChange={(event) => {
                setFile(event.target.files?.[0] ?? null);
                setResultUrl("");
                setStatus("");
              }}
            />
          </label>

          <div className="field">
            <label htmlFor="method">Method</label>
            <select
              id="method"
              value={method}
              onChange={(event) => setMethod(event.target.value)}
            >
              {methods.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </div>

          <div className="field">
            <label htmlFor="factor">Factor: {factor}</label>
            <input
              id="factor"
              max="1"
              min="0.0"
              step="0.01"
              type="range"
              value={factor}
              onChange={(event) => setFactor(Number(event.target.value))}
            />
          </div>

          <button disabled={isLoading} type="submit">
            {isLoading ? <Loader2 className="spin" aria-hidden="true" /> : <Sparkles aria-hidden="true" />}
            Enhance
          </button>

          {status && <p className="status">{status}</p>}
        </form>

        <section className="images" aria-label="Image previews">
          <div className="image-panel">
            <h2>Original</h2>
            {previewUrl ? <img src={previewUrl} alt="Original preview" /> : <div className="placeholder">No image</div>}
          </div>

          <div className="image-panel">
            <h2>Enhanced</h2>
            {resultUrl ? (
              <>
                <img src={resultUrl} alt="Enhanced result" />
                <a className="download" href={resultUrl} download={`enhanced-${file?.name ?? "image"}`}>
                  Download
                </a>
              </>
            ) : (
              <div className="placeholder">Waiting</div>
            )}
          </div>
        </section>
      </section>
    </main>
  );
}
