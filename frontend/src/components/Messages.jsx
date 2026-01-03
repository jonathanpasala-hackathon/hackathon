export default function Messages({ messages }) {
  return (
    <div className="messages">
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
  );
}