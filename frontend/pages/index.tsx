import { useState } from 'react';
import ChatInput from './components/ChatInput'; // Adjust the import path as needed
import ABCMusic from './components/ABCMusic';
import RegenerateButton from './components/RegenerateButton';
import LottieAnimation from './components/LottieMusicAnimation';
import animationData from '../public/lottiemusicanimation.json';

const HomePage = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [musicDetails, setMusicDetails] = useState({
    chords: 'A7 | D7 | E7',
    scales: 'A Major Pentatonic (A B C# E F#)',
    title: '12-Bar Blues Jam Session ',
    style: 'Add a blues swing and rythmic liberty.',
    example: ` 
    M:4/4 
    L:1/8 K:A
    % Harmony - Classic 12-Bar Blues in A
    V:1
    |: "A7"A4 e4 | "D7"d4 f4 | "A7"A4 c4 | "A7"A4 e4 |
    "D7"D4 f4 | "D7"D4 f4 | "A7"A4 c4 | "A7"A4 e4 |
    "E7"E4 g4 | "D7"d4 f4 | "A7"A4 c4 | "E7"E4 g4 :|
  
    % Melody using A Major Pentatonic (A B C# E F#)
    V:2
    |: "A7"A2 B2 C2 E2 | "D7"F2 d2 F2 A2 | "A7"A2 c2 E2 A2 | "A7"A4 B2 c2 |
    "D7"D2 F2 A2 d2 | "D7"D2 F2 A2 d2 | "A7"A2 E2 c2 A2 | "A7"A4 B2 c2 |
    "E7"e2 G2 B2 e2 | "D7"F2 A2 d2 F2 | "A7"A2 B2 c2 A2 | "E7"E4 G2 B2 :|
  `,
  });

  const handleSendMessage = async (message: string) => {
    setIsLoading(true);
    const response = await fetch('http://127.0.0.1:8080/generatejam', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: message }),
    });

    if (!response.ok) {
      console.error('Error fetching music details');
      return;
    }

    const result = await response.json();
    setIsLoading(false);
    setMusicDetails(result); // Update the state with the new music details
    console.log(musicDetails)
  };

  const handleNewSheetMusic = (newExample: string) => {
    setMusicDetails(prevDetails => ({ ...prevDetails, example: newExample }));
  };

  return (
    <div>
      <header>
        <h1>JamSesh.ai</h1>
      </header>
    
      <ChatInput onSendMessage={handleSendMessage} />
      {isLoading && (
        <div className="lottie-overlay">
          <LottieAnimation animationData={animationData} />
        </div>
      )}
      <div>
      {musicDetails.chords && (
        <div className='music-details'>
          <h2>{musicDetails.title}</h2>
          <p><strong>Style:</strong> {musicDetails.style}</p>
          <p><strong>Chords:</strong> {musicDetails.chords}</p>
          <p><strong>Scales:</strong> {musicDetails.scales}</p>
        </div>
      )}
      {musicDetails.example && (
        <div>
          <ABCMusic notation={musicDetails.example} />
          <RegenerateButton musicDetails={musicDetails} onNewMusic={handleNewSheetMusic} setLoading={setIsLoading} />
        </div>
      )}
      </div>

    </div>
  );
};

export default HomePage;
