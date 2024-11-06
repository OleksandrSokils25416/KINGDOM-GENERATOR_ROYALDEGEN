import { useState } from "react";
import "./App.css";
import GenerateButtonComponent from "./components/GenerateButtonComponent";
import OutputTextComponent from "./components/OutputTextComponent";

function App() {
  const [generatedText, setGeneratedText] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false); // New loading state

  const generateText = async (prompt: string, settings: { temperature: number; maxTokens: number }) => {
  setLoading(true);
  try {
    const response = await fetch("http://127.0.0.1:8000/generate-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        temperature: settings.temperature,
        max_tokens: settings.maxTokens,
      }),
    });
    const data = await response.json();
    setGeneratedText(data.text);
  } catch (error) {
    console.error("Error generating text:", error);
    setGeneratedText("Error generating text.");
  } finally {
    setLoading(false);
  }
};


  return (
    <div className="main-container">
      <h1>Kingdom Generator by RoyalDeGen</h1>
      <GenerateButtonComponent onGenerateText={generateText} />
      {loading ? (
          <div className="loading-spinner"></div>
      ):(
      <OutputTextComponent text={generatedText} />
      )}
    </div>
  );
}

export default App;
