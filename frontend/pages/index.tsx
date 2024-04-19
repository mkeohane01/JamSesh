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
  const [harmonyDetails, setHarmonyDetails] = useState(null);
  const [showMelodyExample, setShowMelodyExample] = useState(true);
  const [showHarmonyExample, setShowHarmonyExample] = useState(false);

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
      setHarmonyDetails(null); // Reset the harmony details
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

  const toggleHarmonyExampleVisibility = () => {
    setShowHarmonyExample(!showHarmonyExample);
  };

  const generateHarmony = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8080/genharmony', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(musicDetails),
      });
  
      const data = await response.json();
      setIsLoading(false);
  
      if (!response.ok) {
        throw new Error(data.error || 'Error regenerating music');
      }
  
      setHarmonyDetails(data.harmony);
      console.log('Generated harmony:', harmonyDetails);
    } catch (error) {
      setIsLoading(false);
      console.error('Fetch error:', error.message);
      alert("Please Try Again! error: " + error.message);
    }
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
          <div id="exampleMelodySection" className="section example-melody-section">
            <div className="toggle-container" onClick={toggleMelodyExampleVisibility}>
              <button className={`toggle-button ${showMelodyExample ? 'open' : ''}`}></button>
              <span style={{marginLeft: '8px'}}>Example Melody</span>
            </div>
            {showMelodyExample && (
              <div>
                <ABCMusic notation={musicDetails.example} />
                <RegenerationContainer musicDetails={musicDetails} onNewMusic={handleNewSheetMusic} setLoading={setIsLoading} />
              </div>
            )}
          </div>
        )}
      {musicDetails?.example && (
        <div className="section harmony-section">
          <div className="toggle-container" onClick={toggleHarmonyExampleVisibility}>
            <button className={`toggle-button ${showHarmonyExample ? 'open' : ''}`}></button>
            <span style={{ marginLeft: '8px' }}>Example Harmony</span>
          </div>
          {showHarmonyExample && harmonyDetails && (
            <div>
              <ABCMusic notation={harmonyDetails} />
            </div>
          )}
          {showHarmonyExample && (
            <div>
              <button onClick={generateHarmony} className="generate-harmony-button">Generate Harmony</button>
            </div>
          )}
        </div>      
      )}
      </div>

    </div>
  );
};

export default HomePage;
