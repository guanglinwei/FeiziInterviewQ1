import React from 'react';
import BaseForm from './BaseForm';

function Home() {
    return (<BaseForm submitFormUrl={"/login"}/>)
}

export default Home;