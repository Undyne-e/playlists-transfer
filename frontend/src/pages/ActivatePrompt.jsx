import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api/api";

const ActivatePrompt = () => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [timer, setTimer] = useState(0);

  useEffect(() => {
    if (timer > 0) {
      const interval = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [timer]);

  const handleResendActivation = async () => {
    setLoading(true);
    setMessage("");
    try {
      await api.post("/auth/users/resend_activation/", { email: localStorage.getItem("email") });
      setMessage("Письмо отправлено повторно. Проверьте вашу почту.");
      setTimer(60);
    } catch (error) {
      setMessage("Ошибка при повторной отправке. Попробуйте позже.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg text-center w-96">
        <h2 className="text-2xl font-bold text-white mb-4">Подтвердите Email</h2>
        <p className="text-gray-400 mb-6">
          На вашу почту отправлено письмо с подтверждением. Перейдите по ссылке, чтобы активировать аккаунт.
        </p>
        {message && <p className="text-green-400 mb-4">{message}</p>}
        <button
          onClick={handleResendActivation}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-600"
          disabled={loading || timer > 0}
        >
          {loading ? "Отправка..." : timer > 0 ? `Повторная отправка через ${timer} сек` : "Отправить письмо повторно"}
        </button>
        <Link to="/login" className="text-blue-500 hover:underline block mt-4">
          Вернуться к входу
        </Link>
      </div>
    </div>
  );
};

export default ActivatePrompt;
