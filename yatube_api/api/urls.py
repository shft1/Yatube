from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='post')
router_v1.register(r'posts\/(?P<post_id>\d)\/comments',
                   CommentViewSet, basename='comment')
router_v1.register('groups', GroupViewSet, basename='group')
router_v1.register('follow', FollowViewSet, basename='follow')

path_v1_version = [
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(path_v1_version)),
]
