import { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState("");
  const [loading, setLoading] = useState(false);

  const addMessage = (text, sender, agent = null) => {
    setMessages((prev) => [
      ...prev,
      { text, sender, agent }
    ]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    addMessage(input, "user");
    setInput("");
    setLoading(true);
    setStatus("Processing your request...");
    setStatusType("loading");

    try {
      const res = await fetch("/api/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input })
      });

      if (!res.ok) throw new Error("Network error");

      const data = await res.json();

      if (data.success) {
        addMessage(data.response, "assistant", data.agent);
        setStatus("Request completed successfully");
        setStatusType("success");
      } else {
        addMessage(
          `Error: ${data.error || "Unknown error occurred"}`,
          "assistant"
        );
        setStatus("An error occurred");
        setStatusType("error");
      }
    } catch (err) {
      console.error(err);
      addMessage(
        "Sorry, there was an error processing your request.",
        "assistant"
      );
      setStatus("Connection error");
      setStatusType("error");
    } finally {
      setLoading(false);
      setTimeout(() => setStatus(""), 3000);
    }
  };

  return (
    <div className="chat-app">
      <h1>Chat Assistant</h1>

      <div id="chat-messages" className="messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`message ${msg.sender}-message`}
          >
            <strong>
              {msg.sender === "user" ? "You" : "Assistant"}
              {msg.agent ? ` (${msg.agent.replace("_", " ")})` : ""}:
            </strong>{" "}
            {msg.text}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </form>

      {status && (
        <div className={`status show ${statusType}`}>
          {status}
        </div>
      )}
    </div>
  );
}

export default App;
