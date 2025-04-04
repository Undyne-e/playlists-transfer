#dj
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import PlaylistTransferSerializer, YandexPlaylistTracksSerializer, YouTubePlaylistTracksSerializer, SpotifyPlaylistTracksSerializer

#yandex
from .parsers.yandex_music_api import YandexMusicAPI
from .models import YandexPlaylists, YandexPlaylistTracks

#google
from .parsers.youtube_music_api import YouTubeMusicAPI
from .models import YouTubePlaylists, YouTubePlaylistTracks

#spotify
from .parsers.spotify_api import SpotifyAPI
from .models import SpotifyPlaylists, SpotifyPlaylistTracks


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
                    "user_id": user.id,
                    "title": your_playlist.title,
                    "track_count": your_playlist.track_count,
                    "tracks_downloaded": your_playlist.tracks_downloaded,
                    "source_platform": "yandex_music"
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

            playlist.tracks_downloaded = True
            playlist.save()

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
                            "duration": (track['track']['duration_ms']) if track['track']['duration_ms'] else 0,
                        }
                    )
            return Response({'message': 'Треки плейлиста успешно сохранены'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class YouTubeSavePlaylistsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        token = request.data.get('google_token')
        user = request.user

        if not token:
            return Response({'error': 'Не предоставлен токен YouTube'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            youtube_client = YouTubeMusicAPI(token)
            playlists = youtube_client.get_playlists()

            saved_playlists = []
            for playlist in playlists:
                playlist_obj, created = YouTubePlaylists.objects.update_or_create(
                    user=user,
                    playlist_id=playlist['id'],
                    defaults={  
                        "title": playlist['snippet']['title'],
                        "track_count": playlist['contentDetails']['itemCount'],
                    }
                )

                saved_playlists.append({
                    "youtube_playlist_id": playlist_obj.playlist_id,
                    "user_id": user.id,
                    "title": playlist_obj.title,
                    "track_count": playlist_obj.track_count,
                    "tracks_downloaded": playlist_obj.tracks_downloaded,
                    "source_platform": "youtube_music"
                })

            return Response({"playlists": saved_playlists}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class YouTubeSaveTracksView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        token = request.data.get('google_token')
        playlist_id = request.data.get('youtube_playlist_id')
        user = request.user

        if not token or not playlist_id:
            return Response({'error': 'Токен или ID плейлиста не предоставлены'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            playlist = YouTubePlaylists.objects.filter(user=user, playlist_id=playlist_id).first()
            if not playlist:
                return Response({'error': 'Плейлист не найден в базе. Сначала сохраните список плейлистов.'}, status=status.HTTP_404_NOT_FOUND)
            
            playlist.tracks_downloaded = True
            playlist.save()

            youtube_client = YouTubeMusicAPI(token)
            tracks = youtube_client.get_playlist_tracks(kind=None, playlist_id=playlist_id)

            for track in tracks:
                YouTubePlaylistTracks.objects.update_or_create(
                    playlist=playlist,
                    track_id=track["id"],
                    defaults={
                        "title": track["title"],
                        "artist": track["artist"],
                        "album": "Unknown",
                        "duration": 0 
                    }
                )

            return Response({'message': 'Треки плейлиста успешно сохранены'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class SpotifySavePlaylistsView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        token = request.data.get('spotify_token')
        user = request.user

        if not token:
            return Response({'error': 'Не предоставлен токен'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            spotify_client = SpotifyAPI(token)
            playlists = spotify_client.get_playlists()

            saved_playlists = []
            for playlist in playlists:
                playlist_obj, created = SpotifyPlaylists.objects.update_or_create(
                    user=user,
                    playlist_id=playlist['playlist_id'],
                    defaults={  
                        "title": playlist['title'],
                        "track_count": playlist['track_count']
                    }
                )

                saved_playlists.append({
                    "spotify_playlist_id": playlist_obj.playlist_id,
                    "user_id": user.id,
                    "title": playlist_obj.title,
                    "track_count": playlist_obj.track_count,
                    "tracks_downloaded": playlist_obj.tracks_downloaded,
                    "source_platform": "spotify",
                })
            return Response({"playlists": saved_playlists}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class SpotifySaveTracksView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        token = request.data.get('spotify_token')
        playlist_id = request.data.get('spotify_playlist_id')
        user = request.user

        if not token or not playlist_id:
            return Response({'error': 'Токен или ID плейлиста не предоставлены'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            playlist = SpotifyPlaylists.objects.filter(user=user, playlist_id=playlist_id).first()
            if not playlist:
                return Response({'error': 'Плейлист не найден в базе. Сначала сохраните список плейлистов.'}, status=status.HTTP_404_NOT_FOUND)
            
            playlist.tracks_downloaded = True
            playlist.save()
            
            spotify_client = SpotifyAPI(token)
            tracks = spotify_client.get_playlist_tracks(kind=None, playlist_id=playlist_id, track_count=playlist.track_count)

            for track in tracks:
                SpotifyPlaylistTracks.objects.update_or_create(
                    playlist = playlist,
                    track_id=track["id"],
                    defaults={
                        "title": track["title"],
                        "artist": track["artist"],
                        "album": track["album"],
                        "duration": track["duration"]
                    }
                )
            return Response({'message': 'Треки плейлиста успешно сохранены'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PlaylistTransferViewSet(viewsets.ViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    
    @action(detail=False, methods=["post"])
    def transfer(self, request):
        
        serializer = PlaylistTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        source_platform = serializer.validated_data["source_platform"]
        target_platform = serializer.validated_data["target_platform"]
        playlist_uuid = serializer.validated_data["playlist_uuid"]

        # Получаем треки из YouTube Music
        if source_platform == 'youtube_music':
            try:
                playlist = YouTubePlaylists.objects.get(playlist_id=playlist_uuid)
                tracks = list(YouTubePlaylistTracks.objects.filter(playlist=playlist))
                tracks = [{"artist": t.artist, "title": t.title, "id": t.track_id} for t in tracks]
            except YouTubePlaylists.DoesNotExist:
                return Response({"error": "Плейлист не найден"}, status=404)

        # Получаем треки из Яндекс Музыки
        elif source_platform == 'yandex_music':
            try:
                playlist = YandexPlaylists.objects.get(playlist_uuid=playlist_uuid)
                tracks = list(YandexPlaylistTracks.objects.filter(playlist=playlist))
                tracks = YandexPlaylistTracksSerializer(tracks, many=True).data
            except YandexPlaylists.DoesNotExist:
                return Response({"error": "Плейлист не найден"}, status=404)
        
        # Получаем треки из Spotify
        elif source_platform == 'spotify':
            try:
                playlist = SpotifyPlaylists.objects.get(playlist_id=playlist_uuid)
                tracks = list(SpotifyPlaylistTracks.objects.filter(playlist=playlist))
                tracks = SpotifyPlaylistTracksSerializer(tracks, many=True).data
            except SpotifyPlaylists.DoesNotExist:
                return Response({"error": "Плейлист не найден"}, status=404)
            
        # Переносим в YouTube Music
        if target_platform == 'youtube_music':
            token = request.data.get('google_token')
            if not token:
                return Response({'error': 'Не предоставлен токен'}, status=status.HTTP_400_BAD_REQUEST)

            youtube_client = YouTubeMusicAPI(token)
            new_playlist_id = youtube_client.create_playlist(title=playlist.title)
            unsuccessful_cnt = 0
            not_transferred = []

            for track in tracks[::-1]:
                track_id = youtube_client.search_track(artist=track["artist"], title=track["title"])
                if track_id:
                    youtube_client.add_tracks_to_playlist(playlist_id=new_playlist_id, track_id=track_id, kind=None)
                else:
                    unsuccessful_cnt += 1
                    not_transferred.append({
                        "artist": track["artist"],
                        "title": track["title"],
                    })

            return Response({
                "message": "Плейлист перенесён",
                "not transferred tracks": unsuccessful_cnt,
                "not_transferred": not_transferred
            })

        # Переносим в Яндекс Музыку
        elif target_platform == 'yandex_music':
            token = request.data.get('yandex_token')
            if not token:
                return Response({'error': 'Не предоставлен токен'}, status=status.HTTP_400_BAD_REQUEST)

            yandex_client = YandexMusicAPI(token)
            new_playlist = yandex_client.create_playlist(title=playlist.title)
            unsuccessful_cnt = 0
            not_transferred = []

            for track in tracks[::-1]:
                new_track_id, new_album_id = yandex_client.search_track(artist=track['artist'], title=track['title'])
                if new_track_id and new_album_id:
                    yandex_client.add_tracks_to_playlist(kind=new_playlist.kind, track_id=new_track_id, album_id=new_album_id)
                else:
                    unsuccessful_cnt += 1
                    not_transferred.append({
                        "artist": track["artist"],
                        "title": track["title"],
                    })

            return Response({
                "message": "Плейлист перенесён",
                "not transferred tracks": unsuccessful_cnt,
                "not_transferred": not_transferred
            })
        
        # Переносим в Spotify
        elif target_platform == 'spotify':
            token = request.data.get('spotify_token')
            if not token:
                return Response({'error': 'Не предоставлен токен'}, status=status.HTTP_400_BAD_REQUEST)

            spotify_client = SpotifyAPI(token)
            new_playlist = spotify_client.create_playlist(title=playlist.title)
            unsuccessful_cnt = 0
            not_transferred = []

            for track in tracks:
                new_track_id = spotify_client.search_track(artist=track['artist'], title=track['title'])
                if new_track_id:
                    spotify_client.add_tracks_to_playlist(kind=new_playlist, track_id=new_track_id, album_id=None)
                else:
                    unsuccessful_cnt += 1
                    not_transferred.append({
                        "artist": track["artist"],
                        "title": track["title"],
                    })

            return Response({
                "message": "Плейлист перенесён",
                "not transferred tracks": unsuccessful_cnt,
                "not_transferred": not_transferred
            })

        return Response({"error": "Неизвестная целевая платформа"}, status=400)




