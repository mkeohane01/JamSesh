import { useState } from 'react';
import ChatInput from './components/ChatInput'; // Adjust the import path as needed
import ABCMusic from './components/ABCMusic';
import RegenerationContainer from './components/RegenerationContainer';
import LottieAnimation from './components/LottieMusicAnimation';
import animationData from '../public/lottiemusicanimation.json';

const HomePage = () => {
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
    try {
      const response = await fetch('http://127.0.0.1:8080/generatejam', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: message }),
      });
  
      const data = await response.json(); // Parse the JSON data first
      setIsLoading(false);
  
      if (!response.ok) {
        throw new Error(data.error || 'Error fetching music details'); // Use the error message from the response if available
      }
  
      setMusicDetails(data); // Update the state with the new music details
    } catch (error: any) {
      setIsLoading(false);
      console.error('Fetch error:', error.message);
      alert("Please Try Again! error: " + error.message); // Alert the error message or set it in state to display in the UI
    }
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
          <RegenerationContainer musicDetails={musicDetails} onNewMusic={handleNewSheetMusic} setLoading={setIsLoading} />
        </div>
      )}
      </div>

    </div>
  );
};

export default HomePage;
