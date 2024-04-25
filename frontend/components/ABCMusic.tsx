import React, { useState, useEffect, useRef } from 'react';
import abcjs from 'abcjs';
import '../node_modules/abcjs/abcjs-audio.css';

interface ABCMusicProps {
  notation: string;
  className?: string;
  showAudio?: boolean;
}

const ABCMusic: React.FC<ABCMusicProps> = ({ notation, className, showAudio = true }) => {
  const paperRef = useRef<HTMLDivElement>(null);
  const audioRef = useRef<HTMLDivElement>(null);
  const [chordsOff, setChordsOff] = useState(false);
  const [voicesOff, setVoicesOff] = useState(false);

  useEffect(() => {
    if (!notation || !paperRef.current) {
      console.error("No notation provided or the DOM ref is not available.");
      return;
    }

    const visualOptions = {
      staffwidth: 500,
      expandToWidest: true,
      jazzchords: true,
      scale: 1.2,
      responsive: "resize" as "resize"
    };

    // Safely attempt to render ABC notation
    let visualObj : any = null;
    try {
      visualObj = abcjs.renderAbc(paperRef.current, notation, visualOptions);
    } catch (error) {
      console.error("Error rendering ABC notation:", error);
      return;
    }

    if (showAudio) {
      const activateAudio = async () => {
        if (!abcjs.synth.supportsAudio()) {
          console.log("Audio is not supported on this browser.");
          return;
        }

        const synthControl = new abcjs.synth.SynthController();
        if (audioRef.current) {
          synthControl.load(audioRef.current, null, {
            displayLoop: true,
            displayRestart: true,
            displayPlay: true,
            displayProgress: true,
            displayWarp: true
          });
        }

        try {
          const createSynth = new abcjs.synth.CreateSynth();
          await createSynth.init({ visualObj: visualObj[0] });
          await synthControl.setTune(visualObj[0], false, {
            chordsOff: chordsOff,
            voicesOff: voicesOff,
          });
          console.log("Audio is ready for playback.");
        } catch (error) {
          console.error("Failed to load audio:", error);
        }
      };

      activateAudio();
    }
  }, [notation, chordsOff, voicesOff]);

  return (
    <div className={className ? className : "sheet-music-container"}>
      <div ref={paperRef} className="sheet-music"/>
      {showAudio && (
        <>
          <div ref={audioRef} />
          <label>
            <input
              type="checkbox"
              checked={chordsOff}
              onChange={(e) => setChordsOff(e.target.checked)}
            /> Turn off chords
          </label>
          <label>
            <input
              type="checkbox"
              checked={voicesOff}
              onChange={(e) => setVoicesOff(e.target.checked)}
            /> Turn off melody
          </label>
        </>
      )}
    </div>
  );
};

export default ABCMusic;
