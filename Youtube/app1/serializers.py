from rest_framework.serializers import ModelSerializer
from .models import *

class ProfilSer(ModelSerializer):
    class Meta:
        model = Profil
        fields = '__all__'

class VideoSer(ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class PlaylistSer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'

class CommentSer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'