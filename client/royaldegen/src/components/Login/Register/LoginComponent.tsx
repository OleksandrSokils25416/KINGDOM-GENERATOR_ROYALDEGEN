import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useUserContext } from "../../../context/UserProvider.tsx";

function Login() {
  const [usernameInput, setUsernameInput] = useState("");
  const [password, setPassword] = useState("");
  const { username, setUsername } = useUserContext();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await fetch("https://royaldegeneratorback-dnazb5haeufsevec.polandcentral-01.azurewebsites.net//login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: usernameInput, password }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("accessToken", data.access_token);
        setUsername(usernameInput);
        navigate("/");
      } else {
        alert("Login failed");
      }
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    setUsername(null);
    navigate("/login");
  };

  return (
    <div className="auth-container">
      {username ? (
        <>
          <h2 id="welc-user">Welcome, {username}!</h2>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <h2>Login</h2>
          <input
            type="text"
            value={usernameInput}
            onChange={(e) => setUsernameInput(e.target.value)}
            placeholder="Username"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
          <button onClick={handleLogin}>Login</button>
        </>
      )}
    </div>
  );
}

export default Login;
