import { useState } from "react"
import { analyzeAudio } from "./services/api"

function AudioUploader({ onAnalysisComplete }) {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]

    if (selectedFile) {
      setFile(selectedFile)
      setResult(null)
      setError("")
    }
  }

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select an audio file first.")
      return
    }

    try {
      setLoading(true)
      setError("")
      setResult(null)

      const data = await analyzeAudio(file)

      setResult(data)
      onAnalysisComplete(data)

    } catch (err) {
      setError(
        err.message || "Could not connect to the SVARA-X backend."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card audio-uploader">

      <div className="card-label">
        AUDIO INPUT
      </div>

      <h3>Upload Voice Sample</h3>

      <p>
        Select an audio recording for SVARA-X analysis.
      </p>

      <input
        type="file"
        accept="audio/*"
        onChange={handleFileChange}
      />

      {file && (
        <>
          <div className="selected-file">
            🎙️ {file.name}
          </div>

          <button
            className="analyze-btn"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading
              ? "🔄 SENDING TO SVARA-X..."
              : "🎙 ANALYZE AUDIO"}
          </button>
        </>
      )}

      {error && (
        <div className="selected-file">
          ⚠️ {error}
        </div>
      )}

      {result && (
        <div className="selected-file">
          ✅ Backend received: {result.filename}
          <br />
          🛡️ Trust Score: {result.trust_score}
        </div>
      )}

    </div>
  )
}

export default AudioUploader