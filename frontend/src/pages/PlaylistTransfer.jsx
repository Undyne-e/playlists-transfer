import React, { useState, useEffect } from "react";
import Select from "react-select";

const PlaylistTransfer = () => {
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [targetPlatform, setTargetPlatform] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const djoserToken = localStorage.getItem("access_token");
  const YandexToken = localStorage.getItem("yandex_token");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/yandex/get_playlists/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${djoserToken}`,
      },
      body: JSON.stringify({ yandex_token: YandexToken }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Ответ API:", data);
        setPlaylists(Array.isArray(data.playlists) ? data.playlists : []); // Берём массив
        setLoading(false);
      })
      .catch((err) => {
        console.error("Ошибка загрузки плейлистов:", err);
        setError("Ошибка загрузки плейлистов.");
        setLoading(false);
      });
  }, []);
  

  const platformOptions = [
    { value: "yandex_music", label: "Яндекс Музыка" },
    { value: "spotify_music", label: "Spotify" },
    { value: "apple_music", label: "Apple Music" },
  ];

  const platformLabels = {
    yandex_music: "Яндекс Музыка",
    spotify_music: "Spotify",
    apple_music: "Apple Music",
  };

  const handleTransfer = () => {
    if (!selectedPlaylist || !targetPlatform) {
      setStatus("Выберите плейлист и платформу!");
      return;
    }

    setStatus("Перенос в процессе...");

    fetch("http://127.0.0.1:8000/api/v1/playlist-transfer/transfer/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${djoserToken}`,
      },
      body: JSON.stringify({
        yandex_token: YandexToken,
        source_platform: selectedPlaylist.source_platform,
        target_platform: targetPlatform.value,
        playlist_uuid: selectedPlaylist.value,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setStatus(`Ошибка: ${data.error}`);
        } else {
          setStatus("Плейлист успешно перенесён!");
        }
      })
      .catch(() => setStatus("Ошибка при переносе!"));
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
          <div className="space-y-4">
            <Select
              options={playlists.map((pl) => ({
                value: pl.yandex_playlist_uuid || pl.spotify_playlist_uuid || pl.apple_playlist_uuid,
                label: `${pl.title} (${pl.track_count} треков) - ${platformLabels[pl.source_platform]}`,
                source_platform: pl.source_platform,
              }))}
              onChange={setSelectedPlaylist}
              placeholder="Выберите плейлист"
              className="mb-4 text-black"
            />

            <h3 className="text-lg font-semibold text-white">Выберите платформу</h3>
            <Select
              options={platformOptions}
              onChange={setTargetPlatform}
              placeholder="Выберите сервис"
              className="mb-4 text-black"
            />

            <button
              onClick={handleTransfer}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition"
            >
              Перенести
            </button>

            {status && <p className="mt-4 text-center font-semibold text-white">{status}</p>}
          </div>
        )}

        <button
          onClick={() => window.history.back()}
          className="mt-6 w-full bg-gray-600 text-white py-2 px-4 rounded-lg hover:bg-gray-700 transition"
        >
          Вернуться назад
        </button>
      </div>
    </div>
  );
};

export default PlaylistTransfer;
