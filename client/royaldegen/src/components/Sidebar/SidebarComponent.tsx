import React, { useState } from "react";
import { Link } from "react-router-dom";
import { FaHome, FaUserCircle } from "react-icons/fa";
import "./SidebarComponent.css";

const SidebarComponent = () => {
  const [isExpanded, setIsExpanded] = useState(true);

  const toggleSidebar = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className={`sidenav ${isExpanded ? "expanded" : "collapsed"}`}>
      <button className="expand-button" onClick={toggleSidebar}>
        ☰
      </button>

      <ul>
        <li>
          <Link to="/">
            <FaHome className="icon" />
            <span className="text">Home</span>
          </Link>
        </li>
        <li>
          <Link to="/login">
            <FaUserCircle className="icon" />
            <span className="text">Login</span>
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default SidebarComponent;
