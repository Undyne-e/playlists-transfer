import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/api';

const AccountSettings = () => {
  const [username, setUsername] = useState('');

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get('/auth/users/me/');
        setUsername(response.data.username);
      } catch (error) {
        console.error('Failed to fetch user:', error);
      }
    };
    fetchUser();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-900 text-white">
      <h2 className="text-2xl font-bold mb-6">{username}</h2>
      <Link to="/logout" className="text-blue-500 hover:underline mb-4">Выйти</Link>
      <Link to="/deleteaccount" className="text-red-500 hover:underline">Удалить аккаунт</Link>
    </div>
  );
};

export default AccountSettings;
