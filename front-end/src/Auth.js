import React from "react";
import umcg_logo from './umcg-logo.png';
import rug_logo from './rug-logo.png'
import './Auth.css';

function Auth() {
    return (
        <div className="Auth">
            <div className="header">
                <img src="{ umcg-logo }" alt="UMCG Logo" className="logo left"/>
                <h2>Gait Diagnosis System UMCG</h2>
                <img src="{ rug-logo }" alt="University of Groningen Logo" className="logo right"/>
            </div>
            <div className="form-box">
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
