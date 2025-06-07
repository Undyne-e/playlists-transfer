import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/api';

const Logout = () => {
    const navigate = useNavigate();
  
    const handleLogout = async () => {
      try {
        await api.post('/auth/token/logout/');
        localStorage.clear();
        navigate('/login');
      } catch (error) {
        console.error('Logout failed:', error);
      }
    };
  
    return (
      <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-900 text-white">
        <h2 className="text-2xl font-bold mb-6">Выход</h2>
        <button onClick={handleLogout} className="bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition">
          Выйти
        </button>
      </div>
    );
  };
  
  export default Logout;