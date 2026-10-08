// api.js - talks to the Flask backend
const API_URL = 'http://127.0.0.1:5000';

async function apiPredict(target, payload) {
  const res = await fetch(`${API_URL}/predict/${target}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Prediction failed');
  return data.prediction;
}
