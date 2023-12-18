import React, {useState} from 'react';
import './style.css';
import {useNavigate} from "react-router-dom";
import config from "./config";
import axios from "axios";

const Login = () => {
    const navigate = useNavigate();
    let [email, setEmail] = useState("");
    let [password, setPassword] = useState("");
    let [errors, setErrors] = useState("");
    let [error, setError] = useState("");
    const [isLoggingin, setisLoggingin] = useState(false);

    const baseURL = config.baseURL;
    let signinEndpoint = "login/";

    const handleLogin = async (e) => {
        e.preventDefault();
        setErrors("");
        setError("");
        try{
            setisLoggingin(true);
            let response = await axios.post(`${baseURL}${signinEndpoint}`, {
                email,
                password
            });
            if (response.status === 200){
                setErrors("");
                localStorage.setItem("_r", response.data.token.refresh);
                localStorage.setItem("_a", response.data.token.access);
                navigate("/");
            }
        } catch (error) {
        e.preventDefault();
        if (error.response && error.response.status === 401) {
            setError(error.response.data.errors.non_field_errors[0]);
        } if (error.response && error.response.status === 400) {
            setErrors(error.response.data.errors);
        }
        } finally {
            setisLoggingin(false);
          }
    }

    return (
      <div className="background">
          <div className="shape"></div>
          <div className="shape"></div>
          <form>
              <h3>Login Here</h3>
              {error && <p style={{ color: "red", fontSize: "15px", marginTop: "30px", textAlign: "center" }}>{error}</p>}
              <label htmlFor="email">Email</label>
              <input type="text" placeholder="example@example.com" id="email"
              onChange={(e) => setEmail(e.target.value)}
                style={{ border: (errors.email || error ) ? "1px solid red" : "" }}/>
                {errors.email && (
                  <p style={{ color: "red", fontSize: "12px" }}>{errors.email[0]}</p>
                )}
              <label htmlFor="password">Password</label>
              <input type="password" placeholder="Password" id="password"
              onChange={(e) => setPassword(e.target.value)}
                style={{ border: (errors.password || error ) ? "1px solid red" : "" }}/>
              {errors.password && (
                  <p style={{ color: "red", fontSize: "12px" }}>{errors.password[0]}</p>
                )}
              <button onClick={handleLogin}>Log In</button>

              <div className="social">
                  <button onClick={() => navigate("/signup/")} className="signup">Sign Up</button>
              </div>
          </form>
          {isLoggingin && (
            <div className="overlay">
              <div className="loader"></div>
            </div>
        )}
      </div>
    );
};

export default Login;
