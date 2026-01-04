import { useState } from "react";
import Chat from "./components/Chat";
import { processMessage, clearConversation } from "./services/api";

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
    <Chat
      messages={messages}
      input={input}
      setInput={setInput}
      onSubmit={handleSubmit}
      onClear={handleClearConversation}
      loading={loading}
      status={status}
      statusType={statusType}
    />
  );
}

export default App;
