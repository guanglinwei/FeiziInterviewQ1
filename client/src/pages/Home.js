import React from 'react';
import BaseForm from './BaseForm';

function Home() {
    return (<BaseForm submitFormUrl={"/login"} submitButtonText={"Log in"} title={"Log In"}/>)
}

export default Home;