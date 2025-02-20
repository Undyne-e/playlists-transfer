from abc import ABC, abstractmethod

class BaseMusicAPI(ABC):

    @abstractmethod
    def authenticate(self, token: str):
        """Авторизация через OAuth-токен."""
        pass

    @abstractmethod
    def get_playlists(self):
        """Получение списка плейлистов пользователя."""
        pass

    @abstractmethod
    def get_playlist_tracks(self, playlist_id: str):
        """Получение треков из плейлиста."""
        pass

    @abstractmethod
    def create_playlist(self, name: str, description: str):
        """Создание нового плейлиста."""
        pass

    @abstractmethod
    def add_tracks_to_playlist(self, playlist_id: str, tracks: list):
        """Добавление треков в плейлист."""
        pass