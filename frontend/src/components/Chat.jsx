import MessageList from "./Messages";
import ChatInput from "./ChatInput";
import StatusBar from "./StatusBar";
import "./ChatStyle.css";
import { useState } from "react";
import { processMessage } from "../services/api";
import { useEffect } from "react";


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

  return (
    <div className="chat-app">
      <div className="chat-header"> {/* header div*/}
        <h1>Chat Assistant</h1>
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