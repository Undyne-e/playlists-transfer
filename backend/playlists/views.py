#dj
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import PlaylistTransferSerializer, YandexPlaylistTracksSerializer

#yandex
import yandex_music
from .parsers.yandex_music_api import YandexMusicAPI
from .models import YandexPlaylists, YandexPlaylistTracks

#google
from .parsers.youtube_music_api import YouTubeMusicAPI
from .models import YouTubePlaylists, YouTubePlaylistTracks


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
        user_id = request.data.get('user_id')
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
            print(playlists[0])

            saved_playlists = []
            for playlist in playlists:
                playlist_obj, created = YouTubePlaylists.objects.update_or_create(
                    user=user,
                    playlist_id=playlist['id'],
                    defaults={  
                        "title": playlist['snippet']['title'],
                        #"track_count": playlist['contentDetails']['itemCount']
                    }
                )

                saved_playlists.append({
                    "youtube_playlist_id": playlist_obj.playlist_id,
                    "user_id": user.id,
                    "title": playlist_obj.title,
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

        if source_platform == 'yandex_music':
            try:
                playlist = YandexPlaylists.objects.get(playlist_uuid=playlist_uuid)
                tracks = list(YandexPlaylistTracks.objects.filter(playlist=playlist))
                tracks = YandexPlaylistTracksSerializer(tracks, many=True).data
            except YandexPlaylists.DoesNotExist:
                return Response({"error": "Плейлист не найден"}, status=404)
            
        #другие сервисы...



        if target_platform == 'yandex_music':
            token = request.data.get('yandex_token')

            if not token:
                return Response({'error': 'Не предоставлен токен'}, status=status.HTTP_400_BAD_REQUEST)
            
            yandex_client = YandexMusicAPI(token)
            new_playlist = yandex_client.create_playlist(title=playlist.title)
            unsuccessful_cnt = 0

            for track in tracks:
                new_track_id, new_album_id = yandex_client.search_track(artist=track['artist'], title=track['title'])
                if new_track_id and new_album_id: yandex_client.add_tracks_to_playlist(kind=new_playlist.kind, track_id=new_track_id, album_id=new_album_id)
                else: unsuccessful_cnt+=1
            
            return Response({
                "message": "Плейлист перенесён",
                "not transferred tracks": unsuccessful_cnt
            })



