from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app1.views import ProfViewSet, CommentViewSet, PlaylistViewSet, VideoAPIView, CommentAPIView
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

# r = DefaultRouter()
# r.register('user', ProfViewSet)
# r.register('video', VideoViewSet)
# r.register('playlist', PlaylistViewSet)
# r.register('comment', CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(r.urls)),
    path('get_token/', TokenObtainPairView.as_view()),
    path('upd_token/', TokenRefreshView.as_view()),
    path('video/', VideoAPIView.as_view()),
    path('video/<int:pk>/', VideoAPIView.as_view()),
    path('video/<int:pk>/comments/', CommentAPIView.as_view()),
]
