import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // Для навигации

const YandexSavePlaylists = () => {
  const [playlists, setPlaylists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [downloadedPlaylists, setDownloadedPlaylists] = useState([]); // Для хранения скачанных плейлистов
  const djoserToken = localStorage.getItem('access_token');
  const YandexToken = localStorage.getItem('yandex_token');
  const navigate = useNavigate(); // Хук для навигации

  useEffect(() => {
    const fetchPlaylists = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/yandex/get_playlists/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${djoserToken}`,
          },
          body: JSON.stringify({ yandex_token: YandexToken }),
        });

        if (!response.ok) {
          throw new Error("Ошибка при загрузке плейлистов");
        }

        const data = await response.json();
        setPlaylists(data.playlists);
      } catch (err) {
        console.error("Ошибка:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPlaylists();
  }, [djoserToken, YandexToken]);

  const saveTracks = async (yandex_playlist_uuid) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/yandex/save_playlists/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${djoserToken}`,
        },
        body: JSON.stringify({
          yandex_token: YandexToken,
          yandex_playlist_uuid: yandex_playlist_uuid,
        }),
      });

      if (!response.ok) {
        throw new Error("Ошибка при сохранении треков");
      }

      const data = await response.json();
      console.log("Треки сохранены:", data);

      // Добавляем скачанный плейлист в состояние
      setDownloadedPlaylists((prev) => [...prev, yandex_playlist_uuid]);
    } catch (err) {
      console.error("Ошибка:", err);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-bold text-white text-center mb-6">Ваши плейлисты</h2>

        {loading ? (
          <p className="text-white text-center">Загрузка...</p>
        ) : error ? (
          <p className="text-red-500 text-center">{error}</p>
        ) : playlists.length === 0 ? (
          <p className="text-white text-center">Плейлисты не найдены</p>
        ) : (
          <ul className="space-y-4">
            {playlists.map((playlist) => (
              <li
                key={`${playlist.yandex_playlist_uuid}-${playlist.user_id}`}
                className="flex justify-between items-center bg-gray-700 p-3 rounded-lg"
              >
                <div className="text-white">
                  <p>{playlist.title}</p>
                  <p className="text-sm text-gray-400">{playlist.track_count} треков</p>
                </div>
                <div className="flex items-center">
                  {downloadedPlaylists.includes(playlist.yandex_playlist_uuid) && (
                    <span className="text-green-500 mr-2">✔️</span> // Галочка, если плейлист скачан
                  )}
                  <button
                    onClick={() => saveTracks(playlist.yandex_playlist_uuid)}
                    className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition"
                    disabled={downloadedPlaylists.includes(playlist.yandex_playlist_uuid)} // Делаем кнопку неактивной, если плейлист уже скачан
                  >
                    Загрузить треки
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}

        {/* Кнопка для возврата на главный экран */}
        <button
          onClick={() => navigate("/home")}
          className="mt-6 w-full bg-gray-600 text-white py-2 px-4 rounded-lg hover:bg-gray-700 transition"
        >
          Вернуться на главный экран
        </button>
      </div>
    </div>
  );
};

export default YandexSavePlaylists;