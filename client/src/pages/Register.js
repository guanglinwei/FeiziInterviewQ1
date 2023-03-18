import React from 'react';
import BaseForm from './BaseForm';

function Register() {
    return (<BaseForm submitFormUrl={"/register_user"}/>)
}

export default Register;