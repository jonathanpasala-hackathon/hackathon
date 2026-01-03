export async function processMessage(input) {
  const res = await fetch("/api/process", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input }),
  });

  if (!res.ok) {
    throw new Error("Network error");
  }

  return res.json();
}