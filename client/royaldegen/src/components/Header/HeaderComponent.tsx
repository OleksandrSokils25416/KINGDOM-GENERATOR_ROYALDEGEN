import React from "react";
import "./HeaderComponent.css";

type HeaderProps = {
  toggleSidebar: () => void;
};

const HeaderComponent: React.FC<HeaderProps> = ({ toggleSidebar }) => {
  return (
    <header className="header">
      <button className="expand-button" onClick={toggleSidebar}>
        ☰
      </button>
      <h1>Kingdom Generator</h1>
    </header>
  );
};

export default HeaderComponent;
