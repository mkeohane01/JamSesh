import { useState } from 'react';
import ChatInput from './components/ChatInput'; // Adjust the import path as needed
import MessageList from './components/ResponsesDisplay'; // Adjust the import path as needed
import ABCMusic from './components/ABCMusic'

const HomePage = () => {
  const [messages, setMessages] = useState([]);

  // Example ABC notation for demonstration
  const exampleAbcNotation = `
    X:1
    M:4/4
    K:Cmaj
    V:T1           clef=treble
    % Improvised melody with swing feel
    V:T1
    |: "Cmaj7"E4 D2 E2 | "Amin7"C2 D2 E2 G2 | "Dmin7"F2 E2 D2 C2 | "G7"B,4 A2 G2 |
      "Cmaj7"E4 ^F2 G2 | "Amin7"A2 G2 F2 E2 | "Dmin7"D2 C2 B,2 A,2 | "G7"G4 F2 E2 :|
      "Fmaj7"F2 A2 c4 | "Fm7"e2 d2 c2 A2 | "Bb7"B2 D2 F2 A2 | "Ebmaj7"G2 ^F2 E2 D2 |
      "Amin7"c2 E2 A2 c2 | "D7"d2 F2 A2 d2 | "Gmin7"g2 f2 e2 d2 | "C7"c4 B2 A2 |
    |: "Cmaj7"G2 A2 B2 c2 | "Amin7"a2 g2 f2 e2 | "Dmin7"d2 c2 B2 A2 | "G7"G4 F2 E2 :|
  `;

  // Function to send message and get response
  const handleSendMessage = async (message: string) => {
    // Here you'd handle sending the message and updating the state
    // This is simplified for demonstration
  };

  return (
    <div>
      <h1>JamSesh.ai</h1>
      {/* Uncomment the following line if you wish to display messages */}
      {/* <MessageList messages={messages} /> */}
      <ChatInput onSendMessage={handleSendMessage} />

      <h1>Example Sheet Music</h1>
      <ABCMusic notation={exampleAbcNotation} />

    </div>
  );
};

export default HomePage;
