import React from 'react';
import { Link } from 'react-router-dom';
import { FaUserCircle } from 'react-icons/fa';

const Home = () => {
  return (
    <div className="flex h-screen w-screen bg-gray-900 text-white">
      {/* Боковая панель */}
      <div className="w-1/5 bg-gray-800 flex flex-col items-center p-4">
        <Link to="/accountsettings" className="text-2xl font-bold text-center mb-6">
          <FaUserCircle />
          ваш аккаунт
        </Link>
        {/* Дополнительное пространство для будущих элементов */}
      </div>
      {/* Основное окно */}
      <div className="flex-1 bg-gray-700">
        {/* Пустое пространство для будущего контента */}
      </div>
    </div>
  );
};

export default Home;
