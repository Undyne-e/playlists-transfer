import React, { useEffect } from 'react';
import axios from 'axios';

const GoogleCallback = () => {
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
          console.log('Токены получены:', response.data);
          //localStorage.setItem('google_token', data);
          //navigate("/home"); 

        })
        .catch(error => {
          console.error('Ошибка:', error);
        });
    }
  }, []);

  return <div>Обработка авторизации...</div>;
};

export default GoogleCallback;