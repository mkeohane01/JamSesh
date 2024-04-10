import React, { useState, useRef } from 'react';

interface ChordDisplayProps {
  chordString: string;
}

const ChordDisplay: React.FC<ChordDisplayProps> = ({ chordString }) => {
  const [selectedChord, setSelectedChord] = useState<{ chord: string; x: number; y: number } | null>(null);
  const buttonRefs = useRef<(HTMLButtonElement | null)[]>([]);

  const handleChordClick = (chord: string, index: number) => {
    const button = buttonRefs.current[index];
    if (button) {
      const rect = button.getBoundingClientRect();
      // Check if the clicked chord is already selected. If so, close the popup.
      if (selectedChord && chord === selectedChord.chord) {
        setSelectedChord(null);
      } else {
        setSelectedChord({
          chord,
          x: rect.left + window.scrollX + rect.width / 2,
          y: rect.top + window.scrollY - 60, // Adjust if necessary
        });
      }
    }
  };

  const handleClose = () => {
    setSelectedChord(null);
  };

  return (
    <div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', justifyContent: 'center' }}>
        {chordString.split('|').map((chord, index) => (
          <React.Fragment key={index}>
            <button
              className="chord-button"
              ref={el => buttonRefs.current[index] = el}
              onClick={() => handleChordClick(chord.trim(), index)}
            >
              {chord.trim()}
            </button>
            {((index + 1) % 4 === 0 && index !== chordString.split('|').length - 1) && <div style={{ height: '30px', borderLeft: '2px solid #ffffff', marginLeft: '5px', marginRight: '5px' }} />}
          </React.Fragment>
        ))}
      </div>
      {selectedChord && (
        <div
          className="chord-detail-box"
          style={{ top: `${selectedChord.y}px`, left: `${selectedChord.x}px` }}
        >
          <button className="close-button" onClick={handleClose}>✖</button>
          <h3>{selectedChord.chord}</h3>
          <p>Dummy sheet music for {selectedChord.chord}</p>
        </div>
      )}
    </div>
  );
};

export default ChordDisplay;
