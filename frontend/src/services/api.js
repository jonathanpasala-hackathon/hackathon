export function getOrCreateSessionId() {
  let sessionId = sessionStorage.getItem('chatSessionId');
  if (!sessionId) {
    sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    sessionStorage.setItem('chatSessionId', sessionId);
  }
  return sessionId;
}

export async function processMessage(input) {
  const sessionId = getOrCreateSessionId();

  const res = await fetch("/api/process", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      input,
      session_id: sessionId
    }),
  });

  if (!res.ok) {
    throw new Error("Network error");
  }

  return res.json();
}

export async function clearConversation() {
  const sessionId = getOrCreateSessionId();

  const res = await fetch("/api/clear", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });

  if (!res.ok) {
    throw new Error("Failed to clear conversation");
  }

  return res.json();
}