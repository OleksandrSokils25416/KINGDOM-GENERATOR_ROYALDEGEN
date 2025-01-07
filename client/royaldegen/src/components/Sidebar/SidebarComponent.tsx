import React from "react";
import { Link, useLocation } from "react-router-dom";
import { FaHome, FaUserCircle } from "react-icons/fa";
import "./SidebarComponent.css";

type SidebarProps = {
  isExpanded: boolean;
};

const SidebarComponent: React.FC<SidebarProps> = ({ isExpanded }) => {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path;

  return (
    <div className={`sidenav ${isExpanded ? "expanded" : "collapsed"}`}>
      <ul>
        <li>
          <Link to="/" className={isActive("/") ? "active" : ""}>
            <FaHome className="icon" />
            <span className="text">Home</span>
          </Link>
        </li>
        <li>
          <Link to="/login" className={isActive("/login") ? "active" : ""}>
            <FaUserCircle className="icon" />
            <span className="text">Login</span>
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default SidebarComponent;
