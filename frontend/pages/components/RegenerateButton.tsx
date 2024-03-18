import React from 'react';

const RegenerateButton = ({ musicDetails, onNewMusic, setLoading}) => {
  const handleRegenerate = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8080/regeneratemusic', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(musicDetails),
      });
  
      const data = await response.json(); // Parse the JSON data first
      setLoading(false);
  
      if (!response.ok) {
        throw new Error(data.error || 'Error regenerating music'); // Use the error message from the response if available
      }
  
      onNewMusic(data.examplesong); // Callback to update the music in the parent component
    } catch (error: any) {
      setLoading(false);
      console.error('Fetch error:', error.message);
      alert("Please Try Again! error: " + error.message); // Alert the error message or set it in state to display in the UI
    }
  };

  return (
    <button onClick={handleRegenerate} className="regenerate-button">Regenerate Music</button>
  );
};

export default RegenerateButton;
