import React from 'react';
import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';
import Home from './pages/Home';
import Register from './pages/Register';
import LoginError from './pages/LoginError';
import NotFound from './pages/404';
import LoginSuccess from './pages/LoginSuccess';

function App() {
  
  // const navigate = useNavigate();

  return (
    <BrowserRouter>
      <RoutesComponent/>
    </BrowserRouter>
  );
}

function RoutesComponent() {
  return (
    <Routes>
      <Route path="/" element={<Outlet/>}>
        <Route index element={Home()}/>
        <Route path="register" element={Register()}/>
        <Route path="login_error" element={LoginError()}/>
        <Route path="user" element={LoginSuccess()}/>
        <Route path="*" element={NotFound()}/>
      </Route>
    </Routes>
  );
}

export default App;