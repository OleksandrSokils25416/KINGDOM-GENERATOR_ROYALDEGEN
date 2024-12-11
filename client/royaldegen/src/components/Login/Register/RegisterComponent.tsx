import { useState } from "react";
import "./AuthComponent.css";
import { Link, useNavigate } from "react-router-dom"; // Import Link from react-router-dom

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  // Register.tsx
  const handleRegister = async () => {
    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }), // Include email
      });
      if (response.ok) {
       // alert("Registration successful!");
        navigate("/login");
      } else {
        alert("Registration failed.");
      }
    } catch (error) {
      console.error("Error registering:", error);
      alert("Error registering.");
    }
  };
  return (
    <div className="auth-container">
      <h2>Register</h2>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button onClick={handleRegister}>Register</button>
      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}

export default Register;
