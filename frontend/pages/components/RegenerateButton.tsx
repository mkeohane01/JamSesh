import React from 'react';

const RegenerateButton = ({ musicDetails, onNewMusic }) => {
  const handleRegenerate = async () => {
    const response = await fetch('http://127.0.0.1:8080/regeneratemusic', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(musicDetails),
    });

    if (!response.ok) {
      console.error('Error regenerating music');
      return;
    }

    const { examplesong } = await response.json();
    onNewMusic(examplesong); // Callback to update the music in the parent component
  };

  return (
    <button onClick={handleRegenerate} className="regenerate-button">Regenerate Music</button>
  );
};

export default RegenerateButton;
