from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.generics import ListCreateAPIView

class VideoAPIView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            user = Profil.objects.get(user = request.user)
            videos = Video.objects.filter(user = user)
            # videos = Video.objects.all()
            ser = VideoSer(videos, many=True)
            return Response(ser.data)
        else:
            video = Video.objects.get(id = pk)
            user = Profil.objects.get(user=request.user)
            if video.user == user:
                ser = VideoSer(video)
                return Response(ser.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        data = request.data
        user = Profil.objects.get(user=request.user)
        data['user'] = user.id
        ser = VideoSer(data = data)
        if ser.is_valid():
            ser.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        video = Video.objects.get(id = pk)
        user = Profil.objects.get(user=request.user)
        if video.user == user:
            video.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        video = Video.objects.get(id=pk)
        user = Profil.objects.get(user=request.user)
        data = request.data
        data['user'] = user.id
        ser = VideoSer(video, data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        video = Video.objects.get(id=pk)
        user = Profil.objects.get(user=request.user)
        data = request.data
        data['user'] = user.id
        ser = VideoSer(video, data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class CommentAPIView(APIView):
    def get(self, request, pk):
        video = Video.objects.get(id = pk)
        ser = CommentSer(video.videocomments.all(), many=True)
        return Response(ser.data)
    def post(self, request, pk):
        user = Profil.objects.get(user=request.user)
        video = Video.objects.get(id = pk)
        data = request.data
        data['video'] = video.id
        data['user'] = user.id
        ser = CommentSer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfViewSet(ModelViewSet):
    queryset = Profil.objects.all()
    serializer_class = ProfilSer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        users = Profil.objects.filter(user=self.request.user)
        soz = self.request.query_params.get("search")
        if soz is not None:
            users = Profil.objects.annotate(
                similarity=TrigramSimilarity("ism", soz)
            ).filter(similarity__gte=0.1).order_by("-similarity")
        return users

# class VideoViewSet(ModelViewSet):
#     queryset = Video.objects.all()
#     serializer_class = VideoSer
#     permission_classes = [IsAuthenticated,]
#
#     def get_queryset(self):
#         user = Profil.objects.get(user=self.request.user)
#         videos = Video.objects.filter(user = user)
#         soz = self.request.query_params.get("search")
#         if soz is not None:
#             videos = videos.annotate(
#                 similarity=TrigramSimilarity("nom", soz)
#             ).filter(similarity__gte=0.1).order_by("-similarity")
#         return videos
#
#     def perform_create(self, serializer):
#         user = Profil.objects.get(user=self.request.user)
#         ser = VideoSer(data = self.request.data)
#         if ser.is_valid():
#             ser.save()
#             video = Video.objects.last()
#             video.user = user
#             video.save()
#             return ser.data
#         return ser.errors
#
#     def perform_destroy(self, instance):
#         user = Profil.objects.get(user=self.request.user)
#         if instance.user == user:
#             instance.delete()
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     def perform_update(self, serializer):


class PlaylistViewSet(ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        user = Profil.objects.get(user=self.request.user)
        videos = Playlist.objects.filter(user = user)
        soz = self.request.query_params.get("search")
        if soz is not None:
            videos = videos.annotate(
                similarity=TrigramSimilarity("nom", soz)
            ).filter(similarity__gte=0.1).order_by("-similarity")
        return videos

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSer
    permission_classes = [IsAuthenticated,]