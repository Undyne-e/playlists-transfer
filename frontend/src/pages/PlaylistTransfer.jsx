import React, { useState, useEffect } from "react";
import Select from "react-select";

const PlaylistTransfer = () => {
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [targetPlatform, setTargetPlatform] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notTransferredTracks, setNotTransferredTracks] = useState([]);


  const djoserToken = localStorage.getItem("access_token");
  const YandexToken = localStorage.getItem("yandex_token");
  const YouTubeToken = localStorage.getItem("google_token");
  const SpotifyToken = localStorage.getItem("spotify_token")

  useEffect(() => {
    const fetchPlaylists = async () => {
      try {

        // Плейлисты Yandex
        const yandexRes = await fetch("http://127.0.0.1:8000/api/v1/yandex/get_playlists/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${djoserToken}`,
          },
          body: JSON.stringify({ yandex_token: YandexToken }),
        });
        const yandexData = await yandexRes.json();
        
        // Плейлисты Youtube
        const youtubeRes = await fetch("http://127.0.0.1:8000/api/v1/youtube/get_playlists/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${djoserToken}`,
          },
          body: JSON.stringify({ google_token: YouTubeToken }),
        });
        const youtubeData = await youtubeRes.json();

        // Плейлисты Spotify
        const spotifyRes = await fetch("http://127.0.0.1:8000/api/v1/spotify/get_playlists/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${djoserToken}`,
          },
          body: JSON.stringify({ spotify_token: SpotifyToken }),
        });
        const spotifyData = await spotifyRes.json();

        const yandexPlaylists = Array.isArray(yandexData.playlists)
          ? yandexData.playlists
              .filter(pl => pl.tracks_downloaded) // фильтруем только скачанные
              .map(pl => ({
                value: pl.yandex_playlist_uuid,
                label: `${pl.title} (${pl.track_count} треков) - Яндекс Музыка`,
                source_platform: "yandex_music",
              }))
          : [];

        const youtubePlaylists = Array.isArray(youtubeData.playlists)
          ? youtubeData.playlists
              .filter(pl => pl.tracks_downloaded)
              .map(pl => ({
                value: pl.youtube_playlist_id,
                label: `${pl.title} (${pl.track_count} треков) - YouTube Music`,
                source_platform: "youtube_music",
              }))
          : [];

        const spotifyPlaylists = Array.isArray(spotifyData.playlists)
          ? spotifyData.playlists
              .filter(pl => pl.tracks_downloaded)
              .map(pl => ({
                value: pl.spotify_playlist_id,
                label: `${pl.title} (${pl.track_count} треков) - Spotify`,
                source_platform: "spotify",
              }))
          : [];

        setPlaylists([...yandexPlaylists, ...youtubePlaylists, ...spotifyPlaylists]);
        setLoading(false);
      } catch (err) {
        console.error("Ошибка загрузки плейлистов:", err);
        setError("Ошибка загрузки плейлистов.");
        setLoading(false);
      }
    };

    fetchPlaylists();
  }, []);

  const platformOptions = [
    { value: "yandex_music", label: "Яндекс Музыка" },
    { value: "youtube_music", label: "YouTube Music" },
    { value: "spotify", label: "Spotify" },
  ];

  const handleTransfer = () => {
    if (!selectedPlaylist || !targetPlatform) {
      setStatus("Выберите плейлист и платформу!");
      return;
    }

    setStatus("Перенос в процессе...");

    fetch("http://127.0.0.1:8000/api/v1/transfer/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${djoserToken}`,
      },
      body: JSON.stringify({
        source_platform: selectedPlaylist.source_platform,
        target_platform: targetPlatform.value,
        playlist_uuid: selectedPlaylist.value,
        yandex_token: YandexToken,
        google_token: YouTubeToken,
        spotify_token: SpotifyToken,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setStatus(`Ошибка: ${data.error}`);
          setNotTransferredTracks([]);
        } else {
          setStatus(data.message || "Плейлист успешно перенесён!");
      
          if (data["not_transferred"] && Array.isArray(data["not_transferred"])) {
            setNotTransferredTracks(data["not_transferred"]);
          } else {
            setNotTransferredTracks([]);
          }
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
              options={playlists}
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
            {notTransferredTracks.length > 0 && (
              <div className="mt-4 bg-gray-700 p-4 rounded-lg">
                <h4 className="text-white font-semibold mb-2">Не удалось перенести треки:</h4>
                <ul className="list-disc list-inside text-white text-sm max-h-40 overflow-y-auto">
                  {notTransferredTracks.map((track, index) => (
                    <li key={index}>
                      {track.artist} — {track.title}
                    </li>
                  ))}
                </ul>
              </div>
            )}

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
