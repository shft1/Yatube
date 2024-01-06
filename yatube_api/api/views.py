from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError

from posts.models import Post, Group, Follow
from .serializers import (PostSerializer, CommentSerializer,
                          GroupSerializer, FollowSerializer)
from .permissions import OwnerOrReader


class RetrieveCreateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                            mixins.ListModelMixin):
    """Для получения списка объектов или сохранения объекта."""

    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerOrReader)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


def get_post(kwargs):
    post_id = kwargs.get('post_id')
    post = get_object_or_404(Post, pk=post_id)
    return post


class CommentViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        post = get_post(self.kwargs)
        new_queryset = post.comments.all()
        return new_queryset

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerOrReader)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=get_post(self.kwargs))


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class FollowViewSet(RetrieveCreateViewSet):

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user.username)
        return new_queryset

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following',)

    def perform_create(self, serializer):
        username = self.request.user.username
        following_username = serializer.validated_data.get('following')
        if following_username == username:
            raise ParseError(
                detail='Пользователь не может подписаться на себя!')
        serializer.save(user=self.request.user.username)
