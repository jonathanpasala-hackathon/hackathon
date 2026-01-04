import MessageList from "./Messages";
import ChatInput from "./ChatInput";
import StatusBar from "./StatusBar";
import "./ChatStyle.css";
import { useState, useEffect } from "react";
import { processMessage, clearConversation } from "../services/api";


export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState("");
  const [loading, setLoading] = useState(false);

  console.log("messages length:", messages.length);

  useEffect(() => {
  console.log("Chat mounted");
  return () => console.log("Chat unmounted");
}, []);


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
      const data = await processMessage(input);

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
      setTimeout(() => setStatus(""), 10000);
    }
  };

  const handleClearConversation = async () => {
    try {
      await clearConversation();
      setMessages([{
        text: "Hello! How can I help you today?",
        sender: "assistant",
        agent: null
      }]);
      setStatus("Conversation cleared");
      setStatusType("success");
      setTimeout(() => setStatus(""), 2000);
    } catch (err) {
      console.error("Error clearing conversation:", err);
      setStatus("Failed to clear conversation");
      setStatusType("error");
      setTimeout(() => setStatus(""), 2000);
    }
  };

  return (
    <div className="chat-app">
      <div className="chat-header">
        <h1>Chat Assistant</h1>
        <button
          onClick={handleClearConversation}
          style={{
            padding: "8px 16px",
            backgroundColor: "#dc3545",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "14px"
          }}
        >
          Clear
        </button>
      </div>

      <MessageList messages={messages} />
      <ChatInput
        input={input}
        setInput={setInput}
        onSubmit={handleSubmit}
        loading={loading}
      />
      <StatusBar status={status} type={statusType} />
    </div>
  );
}