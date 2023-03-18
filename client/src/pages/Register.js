import React from 'react';
import BaseForm from './BaseForm';

function Register() {
    return (<BaseForm submitFormUrl={"/register_user"} submitButtonText={"Register"} title={"Register an Account"}/>)
}

export default Register;