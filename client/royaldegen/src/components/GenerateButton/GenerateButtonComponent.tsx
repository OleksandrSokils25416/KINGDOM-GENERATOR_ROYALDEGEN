import { useState } from "react";
import "./GenerateButtonComponent.css";

interface Props {
  onGenerateText: (
    context: string,
    settings: { temperature: number; maxTokens: number }
  ) => void;
}

const GenerateButtonComponent = ({ onGenerateText }: Props) => {
  const [context, setContext] = useState<string>("");
  const [temperature, setTemperature] = useState<number>(0.7);
  const [maxTokens, setMaxTokens] = useState<number>(500);

  const handleGenerateClick = () => {
    onGenerateText(context, { temperature, maxTokens });
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

      <div className="slider-container">
        <label>Temperature: {temperature}</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={temperature}
          onChange={(e) => setTemperature(Number(e.target.value))}
        />

        <label>Max Tokens: {maxTokens}</label>
        <input
          type="range"
          min="100"
          max="1000"
          step="50"
          value={maxTokens}
          onChange={(e) => setMaxTokens(Number(e.target.value))}
        />
      </div>

      <button onClick={handleGenerateClick} className="generate-button">
        Generate
      </button>
    </div>
  );
};

export default GenerateButtonComponent;
