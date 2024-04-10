import { useState } from 'react';
import ChatInput from './components/ChatInput';
import Head from 'next/head';
import ABCMusic from './components/ABCMusic';
import RegenerationContainer from './components/RegenerationContainer';
import LottieAnimation from './components/LottieMusicAnimation';
import animationData from '../public/lottiemusicanimation.json';
import ChordDisplay from './components/ChordDisplay';
import ScaleDisplay from './components/ScaleDisplay';

const HomePage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [musicDetails, setMusicDetails] = useState(null);
  const [showMelodyExample, setShowMelodyExample] = useState(true);

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

  const toggleMelodyExampleVisibility = () => {
    setShowMelodyExample(!showMelodyExample);
  };

  return (
    <div>
      <Head>
        <title>JamSesh.ai</title>
        <meta name="description" content="JamSesh.ai - AI-powered music generation" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
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
      {musicDetails?.chords && (
        <div className='music-details'>
          <h2>{musicDetails.title}</h2>
          <p><strong>Style:</strong> {musicDetails.style}</p>
          <p><strong>Suggested Chord Progression:</strong>
          <ChordDisplay chordString={musicDetails.chords} />
          </p>
          <p><strong>Improvisation Scale:</strong>
          <ScaleDisplay scaleString={musicDetails.scales} />
          </p>
        </div>
      )}
      {musicDetails?.example && (
          <div id="exampleMelodySection" className="example-melody-section">
            <div className="toggle-container" onClick={toggleMelodyExampleVisibility}>
              <button className={`toggle-button ${showMelodyExample ? 'open' : ''}`}></button>
              <span style={{marginLeft: '8px'}}>Example Jam</span>
            </div>
            {showMelodyExample && (
              <div>
                <ABCMusic notation={musicDetails.example} />
                <RegenerationContainer musicDetails={musicDetails} onNewMusic={handleNewSheetMusic} setLoading={setIsLoading} />
              </div>
            )}
          </div>
        )}
      </div>

    </div>
  );
};

export default HomePage;
