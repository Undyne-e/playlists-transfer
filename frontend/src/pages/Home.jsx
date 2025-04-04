import React from 'react';
import { Link } from 'react-router-dom';
import { FaUserCircle, FaArrowRight } from 'react-icons/fa';

const Home = () => {
  // Функции для обработки входа
  const handleGoogleLogin = () => {
    const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    const REDIRECT_URI = 'http://localhost:5173/googlecallback';
    const SCOPE = 'https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/youtube.force-ssl';
    const AUTH_URL = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=${SCOPE}&access_type=offline`;
    window.location.href = AUTH_URL;
  };

  const handleYandexLogin = () => {
    const YANDEX_CLIENT_ID = import.meta.env.VITE_YANDEX_CLIENT_ID;
    const REDIRECT_URI = 'http://localhost:5173/yandexcallback';
    const AUTH_URL = `https://oauth.yandex.ru/authorize?response_type=code&client_id=${YANDEX_CLIENT_ID}&redirect_uri=${REDIRECT_URI}`;
    window.location.href = AUTH_URL;
  };

  const handleSpotifyLogin = () => {
    const SPOTIFY_CLIENT_ID = import.meta.env.VITE_SPOTIFY_CLIENT_ID;
    const REDIRECT_URI = 'http://localhost:5173/spotifycallback';
    const SCOPE = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private';
    const AUTH_URL = `https://accounts.spotify.com/authorize?response_type=code&client_id=${SPOTIFY_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${SCOPE}`;
    window.location.href = AUTH_URL;
  }

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
      <div className="flex-1 bg-gray-700 flex flex-col items-center justify-center">
        {/* Контейнер для кнопок входа и новой кнопки */}
        <div className="flex items-center space-x-8">
          {/* Контейнер для кнопок сервисов */}
          <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-96 space-y-4">
            <h2 className="text-2xl font-bold text-white text-center mb-6">Авторизироваться или Загрузить плейлист из:</h2>
            {/* Кнопка входа через Google */}
            <button
              onClick={handleGoogleLogin}
              className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition"
            >
              YouTube music
            </button>
            {/* Кнопка входа через Yandex */}
            <button
              onClick={handleYandexLogin}
              className="w-full bg-yellow-500 text-white py-2 rounded-lg hover:bg-yellow-600 transition"
            >
              Yandex music
            </button>
            {/* Кнопка входа через Spotify */}
            <button
              onClick={handleSpotifyLogin}
              className="w-full bg-yellow-500 text-white py-2 rounded-lg hover:bg-yellow-600 transition"
            >
              Spotify
            </button>
          </div>
          {/* Стрелочка */}
          <FaArrowRight className="text-white text-2xl" />
          {/* Новая кнопка для перехода на /playlisttransfer */}
          <Link
            to="/playlisttransfer"
            className="bg-red-500 text-white py-2 px-6 rounded-lg hover:bg-red-600 transition flex items-center justify-center text-lg"
          >
            Перенести плейлист
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;