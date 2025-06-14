import React, { useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router-dom";

const GoogleCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');

    if (code) {
      // Отправляем код на бэкенд
      const djoserToken = localStorage.getItem('access_token'); // Токен Djoser
      axios.post('http://localhost:8000/auth/google_callback/', { code },{
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${djoserToken}`,  // Токен Djoser
        },
    })
        .then(response => {
          console.log('Токен получен:', response.data);
          localStorage.setItem('google_token', response.data.google_token);
          navigate("/youtube/saveplaylists"); 

        })
        .catch(error => {
          console.error('Ошибка:', error);
        });
    }
  }, []);

  return <div>Обработка авторизации...</div>;
};

export default GoogleCallback;