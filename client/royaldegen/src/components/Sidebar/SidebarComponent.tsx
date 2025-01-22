import React from "react";
import { Link, useLocation } from "react-router-dom";
import { FaHome, FaUserCircle } from "react-icons/fa";
import { FaPhone } from "react-icons/fa6";
import { IoIosBookmarks } from "react-icons/io";
import { useUserContext } from '../../context/UserProvider.tsx';
import "./SidebarComponent.css";

type SidebarProps = {
  isExpanded: boolean;
};

const SidebarComponent: React.FC<SidebarProps> = ({ isExpanded }) => {
  const location = useLocation();
  const { username } = useUserContext();

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
        {username ? (
          <li>
            <Link to="/login" className={isActive("/login") ? "active" : ""}>
              <FaUserCircle className="icon" />
              <span className="text">{username}</span>
            </Link>
          </li>
        ) : (
          <li>
            <Link to="/login" className={isActive("/login") ? "active" : ""}>
              <FaUserCircle className="icon" />
              <span className="text">Login</span>
            </Link>
          </li>
        )}
        <li>
          <Link to="/prompts" className={isActive("/prompts") ? "active" : ""}>
            <IoIosBookmarks className="icon" />
            <span className="text">Prompts</span>
          </Link>
        </li>
        <li>
          <Link to="/contact" className={isActive("/contact") ? "active" : ""}>
            <FaPhone className="icon" />
            <span className="text">Contact</span>
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default SidebarComponent;
