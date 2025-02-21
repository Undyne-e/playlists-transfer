import React, { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/api";

const ActivateAccount = () => {
  const { uid, token } = useParams();
  const navigate = useNavigate();
  const [message, setMessage] = useState("Активация...");
  const hasActivated = useRef(false); // Флаг для предотвращения двойного запроса

  useEffect(() => {
    if (hasActivated.current) return; // Предотвращаем повторный вызов
    hasActivated.current = true;

    const activateUser = async () => {
      try {
        await api.post("/auth/users/activation/", { uid, token });
        setMessage("Активация успешна! Перенаправляем...");
        setTimeout(() => navigate("/login"), 2000);
      } catch (error) {
        setMessage("Ошибка активации. Попробуйте снова.");
      }
    };

    activateUser();
  }, [uid, token, navigate]);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <p>{message}</p>
    </div>
  );
};

export default ActivateAccount;
