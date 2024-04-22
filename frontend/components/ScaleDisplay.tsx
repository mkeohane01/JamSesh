const ScaleDisplay = ({ scaleString }: { scaleString: string }) => {
    // Extracting the scale name and notes from the scaleString
    const [scaleName, scaleNotesString] = scaleString.split(" (");
    const scaleNotes = scaleNotesString.slice(0, -1).split(" ");
  
    return (
      <div className="scale-display-container">
        <h3>{scaleName}</h3>
        <ul className="scale-notes-list">
            {scaleNotes.map((note, index) => (
            <li key={index}>{note}</li>
            ))}
        </ul>
      </div>
    );
  };
  
  export default ScaleDisplay;
  