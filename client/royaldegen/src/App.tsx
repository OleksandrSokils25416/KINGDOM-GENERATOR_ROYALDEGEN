import { useState } from "react";
import "./App.css";
import GenerateButtonComponent from "./components/GenerateButtonComponent";
import OutputTextComponent from "./components/OutputTextComponent";

function App() {
  const [generatedText, setGeneratedText] = useState<string>("");

  const generateText = async (prompt: string) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/generate-text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      setGeneratedText(data.text);
    } catch (error) {
      console.error("Error generating text:", error);
    }
  };

  return (
    <div className="main-container">
      <h1>Kingdom generator by RoyalDeGen</h1>
      <GenerateButtonComponent onGenerateText={generateText} />
      <OutputTextComponent text={generatedText} />
    </div>
  );
}

export default App;
