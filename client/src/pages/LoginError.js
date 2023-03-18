import React from 'react';
import { Link } from 'react-router-dom';

function LoginError() {
    return (
        <div style={{textAlign: "center"}}>
            <div>User does not exist</div>
            <Link to="/">Go Back</Link>
        </div>
    );
}

export default LoginError;