import React, { useEffect, useRef } from 'react';
import abcjs from 'abcjs';
import '../../node_modules/abcjs/abcjs-audio.css';

interface ABCMusicProps {
  notation: string;
}

const ABCMusic: React.FC<ABCMusicProps> = ({ notation }) => {
  const paperRef = useRef<HTMLDivElement>(null);
  const audioRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!notation) return;

    // Render the ABC notation visually.
    const visualOptions = { responsive: 'resize' };
    const visualObj = abcjs.renderAbc(paperRef.current, notation, visualOptions);

    // Function to activate and load audio when the user requests it.
    const activateAudio = async () => {
      if (!abcjs.synth.supportsAudio()) {
        console.log("Audio is not supported on this browser.");
        return;
      }

      const synthControl = new abcjs.synth.SynthController();
      synthControl.load(audioRef.current, null, {
        displayLoop: true,
        displayRestart: true,
        displayPlay: true,
        displayProgress: true,
        displayWarp: true
      });

      try {
        const createSynth = new abcjs.synth.CreateSynth();
        await createSynth.init({
          visualObj: visualObj[0]
        });
        await synthControl.setTune(visualObj[0], false);
        console.log("Audio is ready for playback.");
      } catch (error) {
        console.error("Failed to load audio:", error);
      }
    };

    // Activate audio upon component mount
    activateAudio();
  }, [notation]);

  return (
    <div className="sheet-music-container">
      <div ref={paperRef} className="sheet-music"/>
      <div ref={audioRef} />
    </div>
  );
};

export default ABCMusic;
