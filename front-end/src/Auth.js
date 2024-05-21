import React from "react";
import './Auth.css';

function Auth() {
    return (
        <div className="Auth">
            <div className="form-box">
                <div className="header">
                    <h2>Login to Gait Diagnosis System</h2>
                </div>
                <form className="auth-box">
                    <div className="input">
                        <p>Username</p>
                        <input type="text" name="username" />
                    </div>
                    <div className="input">
                        <p>Password</p>
                        <input type="password" name="password" />
                    </div>  
                    <button type="submit">Login</button>
                </form>
            </div>
        </div>
    );
}

export default Auth;