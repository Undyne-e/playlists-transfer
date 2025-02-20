import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const YANDEX_BACKEND_URL = "http://localhost:8000/auth/callback";

const YandexCallback = () => {
  const [message, setMessage] = useState("Обработка...");
  const navigate = useNavigate();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const token = localStorage.getItem("access_token"); // Djoser-токен

    if (!code) {
      setMessage("Ошибка: не найден код авторизации.");
      return;
    }
    if (!token) {
      setMessage("Ошибка: пользователь не аутентифицирован.");
      return;
    }

    fetch(`${YANDEX_BACKEND_URL}?code=${code}`, {
      method: "GET",
      mode: "cors", // Добавляем CORS
      headers: {
        "Authorization": `Token ${token}`, // Передаем Djoser-токен
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          setMessage("Токен успешно сохранен!");
          setTimeout(() => navigate("/dashboard"), 2000);
        } else {
          setMessage(`Ошибка: ${data.error || "Что-то пошло не так"}`);
        }
      })
      .catch(() => setMessage("Ошибка сети. Попробуйте еще раз."));
  }, [navigate]);

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-96">
        <h2 className="text-xl font-bold text-white text-center mb-4">{message}</h2>
      </div>
    </div>
  );
};

export default YandexCallback;
