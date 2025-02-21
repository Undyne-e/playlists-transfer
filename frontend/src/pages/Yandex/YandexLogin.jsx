import React, { useEffect } from "react";

const YANDEX_CLIENT_ID = import.meta.env.VITE_YANDEX_CLIENT_ID;
const REDIRECT_URI = "http://localhost:5173/yandexcallback"; // Новый URL на фронте

const YandexLogin = () => {
  const handleLogin = () => {
    const authUrl = `https://oauth.yandex.ru/authorize?response_type=code&client_id=${YANDEX_CLIENT_ID}&redirect_uri=${REDIRECT_URI}`;
    window.location.href = authUrl;
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-bold text-white text-center mb-6">Вход через Яндекс</h2>
        
        <button
          onClick={handleLogin}
          className="w-full bg-yellow-500 text-white py-3 rounded-lg hover:bg-yellow-600 transition"
        >
          Войти через Яндекс
        </button>
      </div>
    </div>
  );
};

export default YandexLogin;
