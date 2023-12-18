import React, { useState } from "react";
import "./style.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import config from "./config";

const Signup = () => {
  const navigate = useNavigate();
  let [name, setName] = useState("");
  let [email, setEmail] = useState("");
  let [password, setPassword] = useState("");
  let [errors, setErrors] = useState("");
  let [error, setError] = useState("");
  const [issignup, setissignup] = useState(false);

  const baseURL = config.baseURL;
  let signupEndpoint = "signup/";

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      setissignup(true);
      let response = await axios.post(`${baseURL}${signupEndpoint}`, {
        name,
        email,
        password,
      });

      if (response.status === 201) {
        setErrors("");
        // localStorage.setItem("_r", response.data.token.refresh);
        // localStorage.setItem("_a", response.data.token.access);
        navigate("/login");
      } else {
        if (response.data.errors) {
          setErrors(response.data.errors);
        } else {
          setError("An unexpected error occurred. Please try again.");
        }
      }
    } catch (error) {
      console.error("Error during registration:", error);
      setError("An unexpected error occurred. Please try again.");
    }finally {
      setissignup(false);
    }
  };
  return (
    <div className="background">
      <div className="shape"></div>
      <div className="shape"></div>
      <form>
        <h3>Signup Here</h3>
        {error && <p style={{ color: "red", fontSize: "15px" }}>{error}</p>}
        <label htmlFor="name">Name</label>
        <input
          type="text"
          placeholder="Pawan Bisht"
          id="name"
          onChange={(e) => setName(e.target.value)}
          style={{ border: errors.name ? "1px solid red" : "" }}
        />
        {errors.name && (
          <p style={{ color: "red", fontSize: "12px" }}>{errors.name[0]}</p>
        )}
        <label htmlFor="email">Email</label>
        <input
          type="text"
          placeholder="example@example.com"
          id="email"
          onChange={(e) => setEmail(e.target.value)}
          style={{ border: errors.email ? "1px solid red" : "" }}
        />
        {errors.email && (
          <p style={{ color: "red", fontSize: "12px" }}>{errors.email[0]}</p>
        )}
        <label htmlFor="password">Password</label>
        <input
          type="password"
          placeholder="Password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ border: errors.password ? "1px solid red" : "" }}
        />
        {errors.password && (
          <p style={{ color: "red", fontSize: "12px" }}>{errors.password[0]}</p>
        )}
        <button onClick={handleSignup}>Sign Up</button>
        <div className="social">
          <button onClick={() => navigate("/login/")} className="signup">
            Login
          </button>
        </div>
      </form>
      {issignup && (
          <div className="overlay">
            <div className="loader"></div>
          </div>
      )}
    </div>
  );
};

export default Signup;
