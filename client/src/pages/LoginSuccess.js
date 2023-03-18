import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function LoginSuccess() {
    const { state } = useLocation();

    return (
        <div style={{textAlign: "center"}}>
            {!!(state?.username) ?
                <h2>Hello {state.username}</h2> :
                <h3>Invalid user</h3>}
            <Link to="/">Go Back</Link>
        </div>
    );
}

export default LoginSuccess;