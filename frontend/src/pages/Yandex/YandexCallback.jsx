import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = "http://localhost:8000/auth/yandex_callback/";

export default function YandexCallback() {
    const navigate = useNavigate();
    const hasFetched = useRef(false); // Флаг, предотвращающий повторный запрос

    useEffect(() => {
        if (hasFetched.current) return; // Если уже запрашивали, выходим
        hasFetched.current = true; // Устанавливаем флаг

        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get("code");
        const djoserToken = localStorage.getItem('access_token');

        if (code && djoserToken) {
            fetch(`${API_URL}?code=${code}`, {
                method: "GET",
                headers: {
                    "Authorization": `Token ${djoserToken}`
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Токен получен:', data);
                localStorage.setItem('yandex_token', data.yandex_token);
                navigate("/yandex/saveplaylists"); 
            })
            .catch(error => console.error("Ошибка запроса:", error));
        } else {
            navigate("/login"); 
        }
    }, [navigate]);

    return <h2>Авторизация...</h2>;
}
