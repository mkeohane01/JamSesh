import React from 'react';

interface Message {
  type: 'user' | 'response';
  content: string;
}

interface MessageListProps {
  messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <ul className="message-list">
      {messages.map((message, index) => (
        <li key={index} className={message.type === 'user' ? 'user-message' : 'response-message'}>
          {message.content}
        </li>
      ))}
    </ul>
  );
};

export default MessageList;
