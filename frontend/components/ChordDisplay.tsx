import React, { useState, useRef } from 'react';
import ABCMusic from './ABCMusic';

interface ChordDisplayProps {
  chordString: string;
}

const ChordDisplay: React.FC<ChordDisplayProps> = ({ chordString }) => {
  const [selectedChord, setSelectedChord] = useState<{ chord: string; x: number; y: number; abcNotation?: string} | null>(null);
  const buttonRefs = useRef<(HTMLButtonElement | null)[]>([]);

  const handleChordClick = async (chord: string, index: number) => {
    const button = buttonRefs.current[index];
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (button) {
      if (selectedChord && chord === selectedChord.chord) {
        setSelectedChord(null);
      } else {
        const rect = button.getBoundingClientRect();
        const x = rect.left + window.scrollX + rect.width / 2;
        const y = rect.top + window.scrollY - 40; // Adjust if necessary
  
        try {
          const response = await fetch(backendUrl+`/getchord?chord=${encodeURIComponent(chord)}`);
          const data = await response.json();
          // console.log(data);
          if (response.ok && data.chord) {
            setSelectedChord({ chord, x, y, abcNotation: data.chord });
          } else {
            throw new Error(data.error || 'Failed to fetch chord notation');
          }
        } catch (error) {
          console.error('Fetch error:', error);
          alert("Unable to show chord details");
        }
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
          {selectedChord.abcNotation && <ABCMusic notation={selectedChord.abcNotation} className="chord-abc" showAudio={false} />}
        </div>
      )}
    </div>
  );
};

export default ChordDisplay;
