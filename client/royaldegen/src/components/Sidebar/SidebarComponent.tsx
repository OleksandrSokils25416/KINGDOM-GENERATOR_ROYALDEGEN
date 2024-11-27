import React from "react";
import { Link } from "react-router-dom";
import { FaHome, FaUserCircle } from "react-icons/fa";
import "./SidebarComponent.css";

type SidebarProps = {
  isExpanded: boolean;
  isVisible: boolean;
};

const SidebarComponent: React.FC<SidebarProps> = ({
  isExpanded,
  isVisible,
}) => {
  return (
    <div
      className={`sidenav ${isExpanded ? "expanded" : ""} ${
        isVisible ? "visible" : ""
      }`}
    >
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
