import React, { useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router-dom";

const SpotifyCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');

    if (code) {
      // Отправляем код на бэкенд
      const djoserToken = localStorage.getItem('access_token'); // Токен Djoser
      axios.post('http://localhost:8000/auth/spotify_callback/', { code },{
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${djoserToken}`,  // Токен Djoser
        },
    })
    .then(response => {
        console.log('Токен получен:', response.data);
        localStorage.setItem('spotify_token', response.data.spotify_token);
        navigate("/spotify/saveplaylists"); 

      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  }
}, []);

return <div>Обработка авторизации...</div>;
};

export default SpotifyCallback;