# 🛡️ Svara_X — AI Real-Time Fraud Call Protection

> **An end-to-end native Android fraud-call detection and protection system designed for Smart India Hackathon (SIH).**

**Svara_X** is an AI-powered real-time fraud call protection system that analyzes conversations during an active phone call, identifies suspicious fraud patterns, calculates a cumulative risk score, and warns the user before sensitive information is compromised.

Unlike traditional spam-call blockers that primarily rely on caller numbers or static databases, Svara_X focuses on **what is actually being said during the conversation**.

---

## 🚨 The Problem

Modern financial scams are becoming increasingly sophisticated.

Fraudsters can impersonate:

* 🏦 Banks and financial institutions
* 🏛️ Government departments
* 👮 Police and cybercrime authorities
* 🎁 Lottery and prize organizations
* 💰 Investment advisors
* 📱 Telecom providers

They use **urgency, fear, impersonation, secrecy, and social engineering** to convince victims to reveal sensitive information such as OTPs, PINs, passwords, card details, or to make fraudulent payments.

Traditional spam detection systems often stop at identifying **who is calling**.

### Svara_X focuses on a different question:

> **"What is happening inside the conversation?"**

Svara_X continuously analyzes conversational signals and combines multiple fraud indicators to determine whether an ongoing call is potentially dangerous.

---

# 🎯 Key Features

### 📞 Real-Time Call Monitoring

Integrates with the Android Telecom subsystem to monitor incoming cellular calls.

### 🎙️ Live Speech Processing

Processes speech through a real-time audio → speech-to-text pipeline.

### 🧠 Multi-Pattern Fraud Detection

Detects **14 different categories of financial and social-engineering scams**.

### 📊 Cumulative Risk Engine

Combines multiple detected indicators and confidence values into a **0–100% risk score**.

### 🔊 Voice Authenticity Analysis

Uses acoustic heuristics such as zero-crossing and harmonic characteristics to identify potential synthetic/deepfake voice cues.

### 🚨 Real-Time Alerts

Issues high-priority heads-up notifications with sound and vibration when a call reaches a dangerous risk level.

### 📱 Dedicated Live Warning Screen

Displays the current risk level, detected indicators, recommendations, and transcript during the call.

### 🧾 Call History & Forensics

Stores analyzed calls with their risk scores and detected fraud indicators for later review.

### 🧪 Safe Demonstration Mode

Includes a scripted multi-stage Bank OTP scam simulator for hackathon demonstrations without requiring a real fraudulent call.

---

# 🏗️ System Architecture

```text
                 ┌───────────────────────────────┐
                 │     Incoming Cellular Call    │
                 │            Phone A             │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
                 ┌───────────────────────────────┐
                 │ Android Telecom Subsystem     │
                 │          API 29+              │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
                 ┌───────────────────────────────┐
                 │ SvaraCallScreeningService     │
                 │                               │
                 │ • Caller number extraction    │
                 │ • Non-blocking CallResponse   │
                 │ • Call state management       │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
                 ┌───────────────────────────────┐
                 │ CallMonitoringService         │
                 │ Foreground Service            │
                 │                               │
                 │ • OFFHOOK detection           │
                 │ • Audio pipeline              │
                 │ • STT pipeline                │
                 └───────────────┬───────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌──────────────────┐      ┌──────────────────┐
          │    Live Mode     │      │    Demo Mode     │
          │                  │      │                  │
          │ MicrophoneAudio  │      │ DemoSpeechToText │
          │ 16kHz PCM Mono   │      │ Scripted Scam    │
          └────────┬─────────┘      └────────┬─────────┘
                   │                         │
                   └────────────┬────────────┘
                                ▼
                    ┌────────────────────────┐
                    │ Android Speech-to-Text │
                    │      Pipeline          │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │     VoiceAnalyzer       │
                    │                        │
                    │ Acoustic voice cues    │
                    │ Synthetic/deepfake     │
                    │ heuristics              │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │     FraudDetector      │
                    │                        │
                    │ 14 Fraud Categories   │
                    │ Regex + Keyword       │
                    │ Pattern Engine         │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │       RiskEngine       │
                    │                        │
                    │ Weighted Risk Score    │
                    │       0–100%           │
                    │                        │
                    │ Recommendation Engine  │
                    └────────────┬───────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌──────────────────┐      ┌──────────────────┐
          │   AlertManager   │      │ LiveCallActivity │
          │                  │      │                  │
          │ Sound + Vibrate  │      │ High Contrast UI │
          │ Heads-Up Alert   │      │ Risk + Evidence  │
          └──────────────────┘      └──────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │    Call Termination    │
                    │        IDLE            │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ CallHistoryRepository  │
                    │                        │
                    │ SQLite / Preferences   │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ CallHistoryActivity    │
                    │                        │
                    │ Audit & Forensic View  │
                    └────────────────────────┘
```

---

# 🔄 End-to-End Detection Pipeline

Svara_X follows a layered detection architecture:

```text
Incoming Call
      ↓
Call Screening
      ↓
Call Answered
      ↓
Audio Capture
      ↓
Speech-to-Text
      ↓
Voice Analysis
      ↓
Fraud Pattern Detection
      ↓
Risk Calculation
      ↓
Real-Time Warning
      ↓
Call History & Forensics
```

Each layer contributes information to the final risk assessment rather than relying on a single signal.

---

# 🧠 14 Fraud Categories

Svara_X currently detects the following fraud patterns:

| #  | Category                   | Example Signal                                      |
| -- | -------------------------- | --------------------------------------------------- |
| 1  | `OTP_REQUEST`              | Requests for OTPs or 6-digit verification codes     |
| 2  | `PIN_REQUEST`              | ATM PIN, UPI MPIN or security-code requests         |
| 3  | `PASSWORD_REQUEST`         | Requests for banking or login credentials           |
| 4  | `CARD_INFORMATION_REQUEST` | CVV, card number or expiry-date requests            |
| 5  | `ACCOUNT_BLOCK_THREAT`     | Threats to block or suspend an account/SIM          |
| 6  | `BANK_IMPERSONATION`       | Claims to be from SBI, HDFC, ICICI, RBI, etc.       |
| 7  | `URGENT_ACTION`            | "Immediately", "within 10 minutes", etc.            |
| 8  | `GOVERNMENT_IMPERSONATION` | Income Tax, Customs, Telecom Department, etc.       |
| 9  | `POLICE_IMPERSONATION`     | Cyber Cell, police or arrest-related threats        |
| 10 | `PAYMENT_REQUEST`          | Processing fees, penalties or immediate transfers   |
| 11 | `REMOTE_ACCESS_REQUEST`    | AnyDesk, TeamViewer, QuickSupport, etc.             |
| 12 | `PRIZE_SCAM`               | Lottery, cashback or lucky-draw claims              |
| 13 | `INVESTMENT_SCAM`          | Guaranteed returns, doubling money, crypto tips     |
| 14 | `SOCIAL_ENGINEERING`       | Secrecy, pressure or instructions not to disconnect |

---

# 📊 Risk Engine

Svara_X does not depend on a single keyword to classify a call as fraudulent.

Instead, multiple indicators contribute to a **cumulative risk score**.

```text
                    ┌──────────────────┐
                    │ Fraud Indicators │
                    └────────┬─────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
       OTP Request      Urgency          Impersonation
           │                 │                 │
           └─────────────────┼─────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │   RiskEngine   │
                    └───────┬────────┘
                            │
                            ▼
                     Risk Score 0–100%
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
            LOW           MEDIUM         HIGH
                                          │
                                          ▼
                                       CRITICAL
                                          │
                                          ▼
                                  User Protection Alert
```

The engine also generates an actionable recommendation based on the detected risk.

---

# 🎙️ Voice Analysis

Svara_X includes a `VoiceAnalyzer` layer that evaluates acoustic characteristics of incoming speech.

Current heuristics include:

* Zero-crossing characteristics
* Harmonic characteristics
* Acoustic irregularities
* Potential synthetic/deepfake voice cues

The voice layer is designed as an additional signal that can complement linguistic fraud detection.

> **Note:** Voice analysis is currently heuristic-based and should not be interpreted as a definitive deepfake detector.

---

# 📂 Project Structure

```text
Svara_X/
│
├── android/
│   └── app/
│       └── src/
│           └── main/
│               ├── AndroidManifest.xml
│               │
│               ├── call/
│               │   ├── SvaraCallScreeningService.kt
│               │   ├── CallStateManager.kt
│               │   └── CallStateReceiver.kt
│               │
│               ├── permission/
│               │   └── PermissionHelper.kt
│               │
│               ├── service/
│               │   └── CallMonitoringService.kt
│               │
│               ├── audio/
│               │   ├── AudioInput.kt
│               │   └── MicrophoneAudioInput.kt
│               │
│               ├── speech/
│               │   ├── SpeechToText.kt
│               │   ├── TranscriptChunk.kt
│               │   ├── AndroidSpeechToText.kt
│               │   └── DemoSpeechToText.kt
│               │
│               ├── fraud/
│               │   ├── FraudCategory.kt
│               │   ├── FraudIndicator.kt
│               │   └── FraudDetector.kt
│               │
│               ├── risk/
│               │   ├── RiskResult.kt
│               │   └── RiskEngine.kt
│               │
│               ├── alert/
│               │   └── AlertManager.kt
│               │
│               ├── voice/
│               │   └── VoiceAnalyzer.kt
│               │
│               ├── history/
│               │   ├── CallRecord.kt
│               │   └── CallHistoryRepository.kt
│               │
│               ├── MainActivity.kt
│               │
│               └── ui/
│                   ├── LiveCallActivity.kt
│                   ├── CallHistoryActivity.kt
│                   └── CallHistoryAdapter.kt
│
├── backend/
│   ├── server.py
│   ├── fraud_detector.py
│   ├── risk_engine.py
│   ├── requirements.txt
│   └── README.md
│
├── src/
│   └── App.tsx
│
└── README.md
```

---

# 📱 Android Components

| Component       | File                           | Responsibility                                      |
| --------------- | ------------------------------ | --------------------------------------------------- |
| Call Screening  | `SvaraCallScreeningService.kt` | Intercepts incoming calls at the Telecom layer      |
| Call State      | `CallStateManager.kt`          | Tracks `IDLE → RINGING → OFFHOOK`                   |
| Permissions     | `PermissionHelper.kt`          | Handles runtime permissions and call-screening role |
| Monitoring      | `CallMonitoringService.kt`     | Orchestrates the active call pipeline               |
| Audio           | `MicrophoneAudioInput.kt`      | Captures 16kHz PCM mono audio                       |
| STT             | `AndroidSpeechToText.kt`       | Native Android speech recognition                   |
| Demo STT        | `DemoSpeechToText.kt`          | Scripted fraud-call simulation                      |
| Fraud Detection | `FraudDetector.kt`             | Detects 14 fraud categories                         |
| Risk Engine     | `RiskEngine.kt`                | Calculates cumulative risk                          |
| Voice Analysis  | `VoiceAnalyzer.kt`             | Acoustic fraud/deepfake heuristics                  |
| Alerting        | `AlertManager.kt`              | Heads-up warning notifications                      |
| Live UI         | `LiveCallActivity.kt`          | Real-time fraud warning interface                   |
| History         | `CallHistoryRepository.kt`     | Stores analyzed call records                        |

---

# 🐍 Python Backend

The project also includes a modular **FastAPI backend**.

```text
backend/
│
├── server.py
├── fraud_detector.py
├── risk_engine.py
├── requirements.txt
└── README.md
```

### API Endpoints

#### Health Check

```http
GET /health
```

Used to verify that the backend service is running.

#### Transcript Analysis

```http
POST /analyze/transcript
```

Accepts transcript data and returns fraud indicators, risk information, and recommendations.

---

# 🌐 Web-Based Simulator

Svara_X also includes a React-based live simulator.

The simulator provides:

* Real-time fraud detection visualization
* Multi-stage scam simulation
* Live warning screen
* Risk-score progression
* Fraud indicator visualization
* Call history
* Android project/codebase viewer
* Demonstration workflow without requiring an actual fraud call

---

# 🧪 Hackathon Demonstration

## Recommended: Demo Mode

For a safe and predictable SIH demonstration, Svara_X includes a scripted **Bank OTP Scam Simulation**.

### Stage 1 — Initial Contact

> "Calling from bank security..."

**Risk: 35% — MEDIUM**

The system identifies the initial bank-impersonation signal.

---

### Stage 2 — Threat Escalation

> "Your account will be blocked within 10 minutes..."

**Risk: 68% — HIGH**

The system combines:

* Bank impersonation
* Account-block threat
* Urgency

The cumulative risk increases.

---

### Stage 3 — Credential Theft Attempt

> "Share the 6-digit OTP right now..."

**Risk: 94% — CRITICAL**

The system detects the critical combination of:

* OTP request
* Urgency
* Bank impersonation
* Account threat

A **heads-up fraud warning** is dispatched.

---

### Stage 4 — Isolation & Pressure

> "Hurry up or the police will freeze your funds..."

**Risk: 98% — CRITICAL**

The system identifies additional:

* Police impersonation
* Urgency
* Threat
* Social engineering

The call remains classified as **CRITICAL**.

---

# 🎬 Demo Flow

```text
Launch Svara_X
      ↓
Shield Status → ACTIVE
      ↓
Run Multi-Stage Scam Simulation
      ↓
Stage 1 → 35% MEDIUM
      ↓
Stage 2 → 68% HIGH
      ↓
Stage 3 → 94% CRITICAL
      ↓
🚨 Fraud Warning
      ↓
Stage 4 → 98% CRITICAL
      ↓
End Call
      ↓
Call Record Saved
      ↓
Call History / Forensic Breakdown
```

---

# 📞 Real Two-Phone Hardware Demonstration

Svara_X can also be demonstrated using two physical Android phones.

### Phone B — Target Device

1. Install Svara_X.
2. Launch the application.
3. Grant the required permissions.
4. Select Svara_X as the default Call Screening application.
5. Ensure **Shield Status** is `ACTIVE`.

### Phone A — Caller Device

1. Place a call to Phone B.
2. Phone B answers the call.
3. Enable **Speakerphone**.
4. Phone A reads the prepared fraud-call script.
5. Svara_X processes the speakerphone audio.
6. Speech is converted into transcript chunks.
7. Fraud indicators are detected.
8. Risk score increases as the conversation progresses.
9. A warning is displayed when the risk reaches a critical level.

> The hardware demonstration uses speakerphone audio as a controlled demonstration protocol because direct access to another party's cellular-call audio is restricted by Android privacy and platform constraints.

---

# 🔐 Privacy & Safety

Svara_X is designed around a **defensive security use case**.

The system is intended to:

* Warn users about suspicious conversations
* Detect social-engineering attempts
* Reduce accidental disclosure of financial credentials
* Provide transparent evidence for why a call was considered risky
* Maintain an audit history for analyzed calls

The demonstration mode uses **synthetic/scripted conversations**, allowing the complete detection pipeline to be demonstrated without interacting with a real fraudster.

---

# ⚙️ Technology Stack

### Android

* Kotlin
* Android Telecom API
* `CallScreeningService`
* `ForegroundService`
* Android `SpeechRecognizer`
* AudioRecord / PCM audio
* RoleManager
* Android Notifications
* SQLite / SharedPreferences
* RecyclerView

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* Regex-based fraud detection
* Risk scoring engine

### Frontend

* React
* TypeScript
* Web-based live simulator

---

# 🧩 Design Philosophy

Svara_X follows a **layered intelligence model**:

```text
WHO is calling?
       +
WHAT are they saying?
       +
HOW are they saying it?
       +
WHAT fraud patterns are present?
       +
HOW many signals are accumulating?
       ↓
FINAL RISK ASSESSMENT
```

This allows Svara_X to move beyond simple caller-ID or keyword-based blocking toward **context-aware real-time fraud protection**.

---

# 🚀 Future Scope

Svara_X can be extended with:

* 🤖 Transformer-based NLP fraud classification
* 🗣️ Advanced speaker verification
* 🎙️ Neural deepfake voice detection
* 🌍 Multilingual Indian-language support
* 📡 Cloud-assisted threat intelligence
* 🧠 Personalized behavioral risk modeling
* 📈 Federated learning for privacy-preserving model improvement
* 🔗 Integration with banking fraud intelligence systems
* 🛡️ On-device AI inference for improved privacy and latency
* 🔄 Continuous threat-pattern updates

---

# 🏆 Smart India Hackathon

**Svara_X** is designed as a practical cybersecurity solution addressing the growing problem of **voice-based financial fraud and social engineering**.

The project combines:

> **Telephony + Speech Processing + AI-Assisted Fraud Detection + Risk Intelligence + Real-Time User Protection**

into a single end-to-end system.

---

# 👥 Project

**Svara_X**

**AI Real-Time Fraud Call Protection**

Built for **Smart India Hackathon (SIH)**

---

## ⭐ If You Find This Project Interesting

Give the repository a ⭐ and explore the implementation.

> **Svara_X — Don't just identify the caller. Understand the conversation.**
