import MessageList from "./Messages";
import ChatInput from "./ChatInput";
import StatusBar from "./StatusBar";

export default function Chat({
  messages,
  input,
  setInput,
  onSubmit,
  onClear,
  loading,
  status,
  statusType,
}) {
  return (
    <div className="chat-app">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Chat Assistant</h1>
        <button
          onClick={onClear}
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
          Clear Conversation
        </button>
      </div>
      <MessageList messages={messages} />
      <ChatInput
        input={input}
        setInput={setInput}
        onSubmit={onSubmit}
        loading={loading}
      />
      <StatusBar status={status} type={statusType} />
    </div>
  );
}