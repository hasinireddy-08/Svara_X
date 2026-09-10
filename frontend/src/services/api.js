const API_URL = "http://localhost:8000"

export async function analyzeAudio(file) {
  const formData = new FormData()
  formData.append("file", file)

  const response = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    throw new Error("Audio analysis failed")
  }

  return await response.json()
}