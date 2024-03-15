import { useState } from 'react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
}

const ChatInput = ({ onSendMessage }: ChatInputProps) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSendMessage(message);
    setMessage('');
  };

  return (
    <form onSubmit={handleSubmit} className="chat-input-container">
      <input
        type="text"
        value={message}
        className ="chat-input"
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
      />
      <button className="send-button" type="submit">Send</button>
    </form>
  );
};

export default ChatInput;