import React, { useState } from 'react';

const RegenerationContainer = ({ musicDetails, onNewMusic, setLoading }) => {
  const [regenprompt, setRegenprompt] = useState('');

  const handleRegenerate = async () => {
    setLoading(true);
    try {
      const updatedMusicDetails = { ...musicDetails, regenprompt }; // Combine musicDetails with the prompt
      const response = await fetch('http://127.0.0.1:8080/regeneratemusic', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedMusicDetails),
      });
  
      const data = await response.json();
      setLoading(false);
  
      if (!response.ok) {
        throw new Error(data.error || 'Error regenerating music');
      }
  
      onNewMusic(data.examplesong);
    } catch (error) {
      setLoading(false);
      console.error('Fetch error:', error.message);
      alert("Please Try Again! error: " + error.message);
    }
  };

  return (
    <div className="regenerate-container">
      <input
        type="text"
        placeholder="Enter regeneration prompt..."
        className="regenerate-input"
        value={regenprompt}
        onChange={(e) => setRegenprompt(e.target.value)}
      />
      <button onClick={handleRegenerate} className="regenerate-button">Regenerate Music</button>
    </div>
  );
};

export default RegenerationContainer;
