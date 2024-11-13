import { useState } from "react";
import "./App.css";
import GenerateButtonComponent from "./components/GenerateButton/GenerateButtonComponent";
import OutputTextComponent from "./components/OutputText/OutputTextComponent";
import Login from "./components/Login/Register/LoginComponent";
import Register from "./components/Login/Register/RegisterComponent";
import SidebarComponent from "./components/Sidebar/SidebarComponent";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";

function App() {
  const [generatedText, setGeneratedText] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const generateText = async (
    prompt: string,
    settings: { temperature: number; maxTokens: number }
  ) => {
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
    <Router>
      <div className="main-container">
        <SidebarComponent />
        <h1>Kingdom Generator by RoyalDeGen</h1>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <GenerateButtonComponent onGenerateText={generateText} />
                {loading ? (
                  <div className="loading-spinner"></div>
                ) : (
                  <OutputTextComponent text={generatedText} />
                )}
              </>
            }
          />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
