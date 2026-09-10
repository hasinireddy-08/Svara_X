import { useState , useEffect} from "react"
import "./App.css"
import AudioUploader from "./AudioUploader"

function App() {
  const [analyzing, setAnalyzing] = useState(false)
  const [complete, setComplete] = useState(false)
  const [liveStage, setLiveStage] = useState("")
  const [trustScore, setTrustScore] = useState(82)
  const [voiceScore, setVoiceScore] = useState(82)
  const [speakerScore, setSpeakerScore] = useState(91)
  const [interactionScore, setInteractionScore] = useState(67)
  const [contextScore, setContextScore] = useState(74)
  const [riskLevel, setRiskLevel] = useState(48)
  const [decision, setDecision] = useState("SAFE — CONTINUE")

  const getVoiceStatus = (score) => {
  if (score >= 80) return "AUTHENTIC"
  if (score >= 60) return "MONITOR"
  return "SUSPICIOUS"
}

const getSpeakerStatus = (score) => {
  if (score >= 85) return "MATCH"
  if (score >= 60) return "PARTIAL MATCH"
  return "MISMATCH"
}

const getInteractionStatus = (score) => {
  if (score >= 80) return "NORMAL"
  if (score >= 60) return "MONITOR"
  return "SUSPICIOUS"
}

const getContextStatus = (score) => {
  if (score >= 80) return "NORMAL PATTERN"
  if (score >= 60) return "UNUSUAL PATTERN"
  return "HIGH RISK PATTERN"
}

  const startLiveAnalysis = async () => {
  try {
    setAnalyzing(true)
    setComplete(false)
    setLiveStage("Requesting microphone access...")

    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
    })

    setLiveStage("Connecting to SVARA-X...")

    const socket = new WebSocket("ws://localhost:8000/ws")

    socket.onopen = () => {
      setLiveStage("Connected — starting live audio analysis...")

      socket.send(
        JSON.stringify({
          type: "start_analysis",
        })
      )

      const mediaRecorder = new MediaRecorder(stream)

      mediaRecorder.ondataavailable = (event) => {
        if (
          event.data.size > 0 &&
          socket.readyState === WebSocket.OPEN
        ) {
          socket.send(event.data)
        }
      }

      mediaRecorder.start(250)

      socket.mediaRecorder = mediaRecorder
      socket.audioStream = stream
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === "status") {
        setLiveStage(data.message)
      }

      if (data.type === "analysis_update") {
        setLiveStage(`${data.stage} — ${data.score}%`)

        if (data.stage === "VOICE AUTHENTICITY") {
          setVoiceScore(data.score)
        }

        if (data.stage === "SPEAKER VERIFICATION") {
          setSpeakerScore(data.score)
        }

        if (data.stage === "INTERACTION DNA") {
          setInteractionScore(data.score)
        }

        if (data.stage === "CONTEXT INTELLIGENCE") {
          setContextScore(data.score)
        }
      }

      if (data.type === "complete") {
        setTrustScore(data.trust_score)
        setRiskLevel(data.risk_level)
        setDecision(data.decision)

        setAnalyzing(false)
        setComplete(true)
        setLiveStage("Analysis complete")

        if (socket.mediaRecorder) {
          socket.mediaRecorder.stop()
        }

        if (socket.audioStream) {
          socket.audioStream.getTracks().forEach((track) => {
            track.stop()
          })
        }

        socket.close()
      }
    }

    socket.onerror = () => {
      setAnalyzing(false)
      setComplete(false)
      setLiveStage("⚠️ WebSocket connection failed")

      stream.getTracks().forEach((track) => {
        track.stop()
      })
    }

    socket.onclose = () => {
      console.log("SVARA-X WebSocket connection closed")
    }

  } catch (error) {
    setAnalyzing(false)
    setComplete(false)

    if (error.name === "NotAllowedError") {
      setLiveStage("⚠️ Microphone permission was denied")
    } else {
      setLiveStage("⚠️ Could not access microphone")
    }
  }
}

  useEffect(() => {
  if (!analyzing) return

 const timer = setTimeout(() => {
  setAnalyzing(false)
  setTrustScore(91)
  setVoiceScore(88)
  setSpeakerScore(95)
  setInteractionScore(79)
  setContextScore(86)
  setRiskLevel(24)
  setDecision("SAFE — CONTINUE")
  setComplete(true)
}, 3000)
  return () => clearTimeout(timer)
}, [analyzing])

  return (
    <div className="dashboard">

      {/* HEADER */}
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">🛡️</div>

          <div>
            <h1>SVARA-X</h1>
            <span>Voice Trust & Impersonation Defense</span>
          </div>
        </div>

        <div className="system-status">
          <div className="status-dot"></div>
          SYSTEM ONLINE
        </div>
      </header>


      {/* MAIN CONTENT */}
      <main className="main">

        <div className="page-heading">
          <p>REAL-TIME SECURITY MONITOR</p>
          <h2>Voice Trust Analysis</h2>
        </div>
        <AudioUploader
  onAnalysisComplete={(data) => {
    setTrustScore(data.trust_score)
    setVoiceScore(data.voice_score)
    setSpeakerScore(data.speaker_score)
    setInteractionScore(data.interaction_score)
    setContextScore(data.context_score)
    setRiskLevel(data.risk_level)
    setDecision(data.decision)
  }}
/>


        {/* TOP SECTION */}
        <section className="top-grid">

          {/* CALLER */}
          <div className="card caller-card">

            <div className="card-label">
              LIVE CALL
            </div>

            <div className="caller">
              <div className="avatar">👤</div>

              <div>
                <strong>Unknown Caller</strong>
                <small>+91 ••••• •••••</small>
              </div>
            </div>

            <div className="live-pill">
              <div className="status-dot"></div>
              {analyzing ? "LIVE ANALYSIS ACTIVE" : " LIVE AUDIO "}
            </div>

            <div className={`waveform ${analyzing ? "waveform-active" : ""}`}>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
            </div>

          </div>


          {/* TRUST CORE */}
          <div className="card trust-card">

            <div className="core">

              <div className="score">
                <strong>{trustScore}</strong>
                <span>TRUST SCORE</span>
              </div>

            </div>

            <div className="safe">
              ● {decision}
            </div>

          </div>


          {/* RISK */}
          <div className="card risk-card">

            <div className="card-label">
              ACTION RISK
            </div>

            <div className="risk-number">
             {riskLevel >= 75 
              ? "HIGH" 
              : riskLevel >= 50 
                ? "MEDIUM" 
                : "LOW"}
</div>

            <p>
  {riskLevel >= 75
    ? "Critical risk detected. The requested action should be blocked or escalated."
    : riskLevel >= 50
      ? "Moderate risk detected. Additional verification is recommended."
      : "Low risk detected. The requested action can continue safely."}
</p>

            <div className="risk-bar">
              <div
                 className="risk-fill"
                 style={{ width: `${riskLevel}%` }}
                ></div>
              </div>

            <div className="card-status">
              RISK LEVEL:{riskLevel}%
            </div>

          </div>

        </section>


        {/* AI ANALYSIS */}
        <section className="analysis-grid">

          {/* VOICE */}
          <div className="card analysis-card">

            <div className="analysis-icon">🎙️</div>

            <h3>VOICE AUTHENTICITY</h3>

            <div className="analysis-score">
              <strong>{voiceScore}</strong>
              <span>%</span>
            </div>

            <div className="progress">
              <div style={{ width: `${voiceScore}%` }}></div>
            </div>

            <div className="card-status">
              {getVoiceStatus(voiceScore)}
            </div>

          </div>


          {/* SPEAKER */}
          <div className="card analysis-card">

            <div className="analysis-icon">👤</div>

            <h3>SPEAKER VERIFICATION</h3>

            <div className="analysis-score">
              <strong>{speakerScore}</strong>
              <span>%</span>
            </div>

            <div className="progress"><div style={{ width: `${speakerScore}%` }}></div>
            </div>

            <div className="card-status">
              {getSpeakerStatus(speakerScore)}
            </div>

          </div>


          {/* INTERACTION */}
          <div className="card analysis-card">

            <div className="analysis-icon">🧬</div>

            <h3>INTERACTION DNA</h3>

            <div className="analysis-score">
              <strong>{interactionScore}</strong>
              <span>%</span>
            </div>

            <div className="progress">
              <div style={{ width: `${interactionScore}%` }}></div>
            </div>

            <div className="card-status">
              {getInteractionStatus(interactionScore)}
            </div>

          </div>


          {/* CONTEXT */}
          <div className="card analysis-card">

            <div className="analysis-icon">🧠</div>

            <h3>CONTEXT INTELLIGENCE</h3>

            <div className="analysis-score">
              <strong>{contextScore}</strong>
              <span>%</span>
            </div>

            <div className="progress">
              <div style={{ width: `${contextScore}%` }}></div>
            </div>

            <div className="card-status">
              {getContextStatus(contextScore)}
            </div>

          </div>

        </section>


        {/* ACTION PANEL */}
        <section className="card action-panel">

          <div className="action-info">

            <div className="warning">
              ⚠️
            </div>

            <div>
              <strong>Adaptive Security Decision</strong>
              <span>
                AI continuously evaluates the call before allowing the requested action.
              </span>
            </div>

          </div>

          <button
  className="analyze-btn"
  onClick={startLiveAnalysis}
>
  {analyzing
    ? "🔄 ANALYZING VOICE..."
    : complete
      ? "✅ ANALYSIS COMPLETE"
      : "🎙 START VOICE ANALYSIS"}
</button>
{liveStage && (
  <div className="selected-file">
    ⚡ {liveStage}
  </div>
)}

        </section>

      </main>

    </div>
  )
}

export default App