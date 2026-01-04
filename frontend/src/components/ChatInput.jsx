import "./ChatInputStyle.css";
import arrow from "../assets/arrow.png";
import loadingIcon from "../assets/loading.gif";

export default function ChatInput({ input, setInput, onSubmit, loading }) {
  const handleKeyDown = (e) => {
    // Enter submits
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSubmit(e);
    }
  };
  return (
    <div className="chat-input-container">
      <form onSubmit={onSubmit} className="chat-input-form">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button type="submit" disabled={loading} className="submit-button">
          {!loading ? (
            <img src={ arrow } alt="arrow"/>
          ): (
            <img src={ loadingIcon } alt="loading"/>
          )}
        </button>
      </form>
    </div>
    
  );
}