import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function BaseForm({ submitFormUrl }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();

    const { state } = useLocation();

    // When the log in button is pressed
    async function submitForm(e) {
        e.preventDefault();

        try {
            const response = await fetch(submitFormUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (!!data.url)
                navigate(data.url, {
                    state: data.state
                });

            setUsername("");
            setPassword("");
            return null;

        } catch (error) {
            console.error("Error: " + error);
        }
    };

    // When component loads
    useEffect(() => {
        setUsername(state?.username || "");
        setPassword("");
    }, [state]);

    return (
        <>
            <h1>Login Page</h1>
            {!!(state?.message) &&
                <div>
                    <h3>{state.message}</h3>
                </div>
            }
            {!!(state?.error) &&
                <div>
                    <h3 style={{color: "red"}}>{state.error}</h3>
                </div>
            }
            <form onSubmit={submitForm}>
                <div>
                    <label htmlFor='username'>Username: </label>
                    <input type='text' id='username' name='username' value={username} onChange={e => setUsername(e.target.value)} />
                </div>
                <div>
                    <label htmlFor='password'>Password: </label>
                    <input type='password' id='password' name='password' value={password} onChange={e => setPassword(e.target.value)} />
                </div>

                <button type='submit'>Login</button>
            </form>
        </>
    );
}

export default BaseForm;