import { useEffect, useState } from "react";
import "./App.css";
import GenerateButtonComponent from "./components/GenerateButton/GenerateButtonComponent";
import OutputTextComponent from "./components/OutputText/OutputTextComponent";
import Login from "./components/Login/Register/LoginComponent";
import Register from "./components/Login/Register/RegisterComponent";
import SidebarComponent from "./components/Sidebar/SidebarComponent";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ParticlesBG from "./components/Particles/ParticlesBG";
import HeaderComponent from "./components/Header/HeaderComponent";
import ContactsComponent from "./components/Contacts/ContactsComponent.tsx";
import PromptsComponent from "./components/Prompts/PromptsComponent.tsx";
import { UserProvider } from "./context/UserProvider.tsx";
import SubsComponent from "./components/Subs/SubsComponent.tsx";

function App() {
  const [generatedText, setGeneratedText] = useState<string>("");
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(true);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768) {
        setIsSidebarExpanded(true);
      } else {
        setIsSidebarExpanded(false);
      }
    };
    handleResize();
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const generateText = async (
    prompt: string,
    settings: { temperature: number; maxTokens: number }
  ) => {
    try {
      const token = localStorage.getItem("accessToken");
      const response = await fetch("https://royaldegeneratorback-dnazb5haeufsevec.polandcentral-01.azurewebsites.net/generate-text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          prompt,
          temperature: settings.temperature,
          max_tokens: settings.maxTokens,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setGeneratedText(data.text);
      } else {
        const errorMessage = await response.text();
        console.error("Error generating text:", errorMessage);
        setGeneratedText("Error generating text.");
      }
    } catch (error) {
      console.error("Error generating text:", error);
      setGeneratedText("Error generating text.");
    }
  };

  const toggleSidebar = () => {
    setIsSidebarExpanded(!isSidebarExpanded);
  };

  return (
    <UserProvider>
      <Router>
      <div className="main-container">
        <HeaderComponent toggleSidebar={toggleSidebar} />
        <SidebarComponent isExpanded={isSidebarExpanded} />
        <main className={`content ${isSidebarExpanded ? "" : "collapsed"}`}>
          <Routes>
            <Route
              path="/"
              element={
                <>
                  <GenerateButtonComponent onGenerateText={generateText} />
                  <OutputTextComponent text={generatedText} />
                </>
              }
            />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/contact" element={<ContactsComponent />} />
            <Route path="/prompts" element={<PromptsComponent />} />
            <Route path="/subscriptions" element={<SubsComponent />} />
          </Routes>
        </main>
        <ParticlesBG />
      </div>
    </Router>
    </UserProvider>
  );
}

export default App;
