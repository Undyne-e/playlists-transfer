import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/api';

const Login = () => {
  const [username, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/token/login/', { username, password });
      localStorage.setItem('access_token', response.data.auth_token);
      navigate('/home');
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-900">
      <form onSubmit={handleLogin} className="bg-gray-800 p-8 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-bold text-white text-center mb-6">Вход</h2>
        
        <input 
          type="username" 
          placeholder="Username" 
          value={username} 
          onChange={(e) => setEmail(e.target.value)} 
          required
          className="w-full p-3 mb-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          required
          className="w-full p-3 mb-6 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        
        <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition">
          Войти
        </button>

        {/* Ссылка для перехода на страницу регистрации */}
        <p className="text-gray-400 text-center mt-4">
          Ещё нет аккаунта?{' '}
          <Link to="/register" className="text-blue-500 hover:underline">
            Зарегистрироваться
          </Link>
        </p>
      </form>
    </div>
  );
};

export default Login;
