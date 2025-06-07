import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/api';

const DeleteAccount = () => {
    const [current_password, setPassword] = useState('');
    const navigate = useNavigate();
    
    const handleDeleteAccount = async (e) => {
      e.preventDefault();
      try {
        await api.delete('/auth/users/me/', { data: { current_password } });
        localStorage.clear();
        navigate('/register');
      } catch (error) {
        console.error('Account deletion failed:', error);
      }
    };
  
    return (
      <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-900 text-white">
        <form onSubmit={handleDeleteAccount} className="bg-gray-800 p-8 rounded-lg shadow-lg w-96">
            <h2 className="text-2xl font-bold text-white text-center mb-6">Удаление аккаунта</h2>

            <input 
                type="password" 
                placeholder="Password" 
                value={current_password} 
                onChange={(e) => setPassword(e.target.value)} 
                required
                className="w-full p-3 mb-6 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition">
                Удалить аккаунт
            </button>
        </form>
      </div>
    );
};
  
export default DeleteAccount;
