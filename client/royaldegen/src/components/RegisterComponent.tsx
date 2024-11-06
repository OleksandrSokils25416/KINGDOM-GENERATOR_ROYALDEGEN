import { useState } from "react";
import "./AuthComponent.css";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");

  // Register.tsx
const handleRegister = async () => {
  try {
      const response = await fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }), // Include email
    });
    if (response.ok) {
      alert("Registration successful!");
    } else {
      alert("Registration failed.");
    }
  } catch (error) {
    console.error("Error registering:", error);
    alert("Error registering.");
  }
};


  return (
      <div className="register-container">
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
      </div>
  );
}

export default Register;
