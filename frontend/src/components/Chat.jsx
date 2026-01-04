import MessageList from "./Messages";
import ChatInput from "./ChatInput";
import StatusBar from "./StatusBar";
import "./ChatStyle.css";


export default function Chat({
  messages,
  input,
  setInput,
  handleSubmit,
  handleClear,
  loading,
  status,
  statusType
}) {

  return (
    <div className="chat-app">
      <div className="chat-header"> {/* header div*/}
        <h1>Chat Assistant</h1>
        <button
          onClick={handleClear}
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