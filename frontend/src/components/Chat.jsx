import MessageList from "./Messages";
import ChatInput from "./ChatInput";
import StatusBar from "./StatusBar";

export default function Chat({
  messages,
  input,
  setInput,
  onSubmit,
  loading,
  status,
  statusType,
}) {
  return (
    <div className="chat-app">
        <h1>Chat Assistant</h1>
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