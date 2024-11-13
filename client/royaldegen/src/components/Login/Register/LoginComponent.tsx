import { useState } from "react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom
import "./AuthComponent.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (response.ok) {
        alert("Login successful!");
      } else {
        alert("Login failed.");
      }
    } catch (error) {
      console.error("Error logging in:", error);
      alert("Error logging in.");
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button onClick={handleLogin}>Login</button>
      <p>
        Don't have an account yet? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}

export default Login;
