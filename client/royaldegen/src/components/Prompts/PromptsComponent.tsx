import React, { useEffect, useState } from "react";
import "./PromptsComponent.css";

type Prompt = {
  id: number;
  user_id: number;
  prompt: string;
  temperature: number;
  max_tokens: number;
  generated_text: string;
  created_at: string | null;
};

const PromptsComponent: React.FC = () => {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [selectedPrompt, setSelectedPrompt] = useState<Prompt | null>(null); // Track selected prompt
  const [error, setError] = useState<string | null>(null);

  const getUsernameFromToken = (token: string): string | null => {
    try {
      console.log("Token received:", token);
      const payloadBase64 = token.split(".")[1];
      const decodedPayload = atob(payloadBase64);
      const payload = JSON.parse(decodedPayload);
      return payload.sub || null;
    } catch (error) {
      console.error("Failed to parse JWT token:", error);
      return null;
    }
  };

  useEffect(() => {
    const fetchPrompts = async () => {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        setError("Please log in to see your prompts.");
        return;
      }

      const username = getUsernameFromToken(token);
      if (!username) {
        setError("Invalid token.");
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:8000/prompts/${username}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          setError(errorData.detail || "Failed to fetch prompts.");
          return;
        }

        const data = await response.json();
        setPrompts(data.prompts || []);
      } catch (err) {
        console.error("Error fetching prompts:", err);
        setError("An error occurred while fetching prompts.");
      }
    };

    fetchPrompts();
  }, []);

  const handlePromptClick = (prompt: Prompt) => {
    setSelectedPrompt(prompt)
  };

  return (
    <div className="contacts-container">
      {error && <p className="error">{error}</p>}
      {selectedPrompt ? (
        <div className="prompt-details">
          <h3>{selectedPrompt.prompt || "Untitled Prompt"}</h3>
          <p>{selectedPrompt.generated_text}</p>
          <button onClick={() => setSelectedPrompt(null)}>Back to list</button>
        </div>
      ) : (
        <>
          {prompts.length === 0 && !error && <p>No prompts found.</p>}
          <ul>
            {prompts.map((prompt) => (
              <li key={prompt.id}>
                <button onClick={() => handlePromptClick(prompt)}>
                  {prompt.prompt || "Untitled Prompt"}
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

export default PromptsComponent;
