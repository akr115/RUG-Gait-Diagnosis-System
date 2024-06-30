import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../AuthContext';
import umcg_logo from '../../umcg-logo.png';
import rug_logo from '../../rug-logo.png';
import './Auth.css';

function Auth() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // Simulate login
    if (username === 'admin' && password === 'password123') {
      login();
      navigate('/upload');
    } else {
      alert('Invalid credentials');
    }
  };

  return (
    <div className="Auth">
      <div className="header">
        <img src={umcg_logo} alt="UMCG Logo" className="logo-left" />
        <h1>Gait Diagnosis System</h1>
        <img src={rug_logo} alt="University of Groningen Logo" className="logo-right" />
      </div>
      <div className="form-box">
        <form className="auth-box" onSubmit={handleLogin}>
          <div className="input">
            <p>Username</p>
            <input
              type="text"
              name="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="input">
            <p>Password</p>
            <input
              type="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

export default Auth;
