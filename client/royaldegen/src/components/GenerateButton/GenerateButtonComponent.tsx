import { useState } from "react";
import "./GenerateButtonComponent.css";

interface Props {
  onGenerateText: (context: string) => void;
}

const GenerateButtonComponent = ({ onGenerateText }: Props) => {
  const [context, setContext] = useState<string>("");

  const handleGenerateClick = () => {
    onGenerateText(context);
  };

  const handleRegenerateClick = () => {
    onGenerateText(context);
  };

  return (
    <div className="generate-button-container">
      <input
        type="text"
        value={context}
        onChange={(e) => setContext(e.target.value)}
        placeholder="Enter a context for text generation"
        className="generate-input"
      />
      <div className="button-group">
        <button onClick={handleGenerateClick} className="generate-button">
          Generate
        </button>
        <button onClick={handleRegenerateClick} className="regenerate-button">
          Regenerate
        </button>
      </div>
    </div>
  );
};

export default GenerateButtonComponent;
