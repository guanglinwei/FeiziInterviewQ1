import React from 'react';
import BaseForm from './BaseForm';
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';

function Home() {
    const navigate = useNavigate();

    const login = useGoogleLogin({
        onSuccess: response => {
            fetch("https://www.googleapis.com/oauth2/v3/userinfo?access_token=" + response.access_token, {
                headers: {
                    "Authorization": "Bearer " + response.access_token,
                    "Accept": "application/json"
                }
            }).then(r => r.json())
                .then((data) => {
                    loginWithGoogle(data);
                });

        },
        onError: () => {
            console.log("Error while logging in with Google");
        }
    });

    async function loginWithGoogle(userData) {
        try {
            // Try logging in to see if account exists
            const response = await fetch("/login", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username: userData.email, isGoogleLogin: 1, sub: userData.sub })
            });

            const data = await response.json();

            let loginData = data;

            if (!!data.url) {
                if (data.url.includes("register")) {
                    // We automatically register if the use doesn't exist if signing in with Google
                    const regResponse = await fetch("/register_user", {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ username: userData.email, isGoogleLogin: 1, sub: userData.sub })
                    });

                    const regData = await regResponse.json();

                    // Then log in again with the newly created user
                    if (!!regData) {
                        const loginResponse = await fetch("/login", {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ username: userData.email, isGoogleLogin: 1, sub: userData.sub })
                        });

                        loginData = await loginResponse.json();
                    }
                }

                // Navigate to the user page
                navigate(loginData.url, {
                    state: loginData.state
                });
            }





            return null;

        } catch (error) {
            console.error("Error: " + error);
        }
    }

    return (
        <div>
            <BaseForm submitFormUrl={"/login"} submitButtonText={"Log in"} title={"Log In"} />
            <br />
            <button
                style={{ padding: "8px 12px", borderRadius: "4px", borderStyle: "solid" }}
                onClick={() => login()}>
                Sign in with Google
            </button>
            {/* <GoogleLogin
                onSuccess={r => handleLoginSuccess(r)}
                onError={() => console.error("Login failed")} /> */}
        </div>
    );
}

export default Home;