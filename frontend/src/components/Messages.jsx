import "./MessagesStyle.css";

export default function Messages({ messages }) {
  return (
     <div className="messages">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`message ${msg.sender}-message`}
        >
          <div className="message-label">
            {msg.sender === "user" ? "You" : "Assistant"}
            {msg.agent ? ` (${msg.agent.replace("_", " ")})` : ""}
          </div>

          <div className="message-bubble">
            {msg.text}
          </div>
        </div>
      ))}
    </div>
  );
}