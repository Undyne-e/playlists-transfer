#dj
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

#yandex
import yandex_music
from .parsers.yandex_music_api import YandexMusicAPI
from .models import YandexPlaylists, YandexPlaylistTracks


class YandexSavePlaylistsView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        token = request.data.get('yandex_token')
        user = request.user

        if not token:
            return Response({'error': 'Не предоставлен токен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            yandex_client = YandexMusicAPI(token)
            playlists = yandex_client.get_playlists()
            playlists_data = [playlist.to_dict() for playlist in playlists]

            saved_playlists = []

            for playlist in playlists_data:
                your_playlist, created = YandexPlaylists.objects.update_or_create(
                    user=user,
                    uid=playlist['owner']['uid'],
                    playlist_uuid=playlist['playlist_uuid'],
                    defaults={  
                        "kind": playlist['kind'],
                        "title": playlist['title'],
                        "track_count": playlist['track_count']
                    }
                )

                saved_playlists.append({
                    "yandex_playlist_uuid": your_playlist.playlist_uuid,
                    "title": your_playlist.title,
                    "track_count": your_playlist.track_count
                })

            return Response({"playlists": saved_playlists}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class YandexSaveTracksView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  

    def post(self, request):

        token = request.data.get('yandex_token')
        playlist_uuid = request.data.get('yandex_playlist_uuid')
        user = request.user

        if not token or not playlist_uuid: Response({'error': 'токен или uuid плейлиста не были предоставлены'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            playlist = YandexPlaylists.objects.filter(user=user, playlist_uuid=playlist_uuid).first()
            if not playlist:
                return Response({'error': 'Плейлист не найден в базе. Сначала сохраните список плейлистов.'}, status=status.HTTP_404_NOT_FOUND)
            
            yandex_client = YandexMusicAPI(token)
            tracks = yandex_client.get_playlist_tracks(playlist.kind, playlist.uid)

            for track in tracks:

                    YandexPlaylistTracks.objects.update_or_create(
                        playlist=playlist,  
                        track_id=track['id'],
                        defaults={
                            "title": track['track']['title'],
                            "artist": track['track']['artists'][0]['name'] if track['track']['artists'] else "Unknown",
                            "album": track['track']['albums'][0]['title'] if track['track']['albums'] else "Unknown",
                            "duration": (track['track']['duration_ms'] // 1000) if track['track']['duration_ms'] else 0,
                        }
                    )
            return Response({'message': 'Треки плейлиста успешно сохранены'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

