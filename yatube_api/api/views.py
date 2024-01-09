from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from posts.models import Follow, Group, Post
from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)
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
        user = self.request.user
        new_queryset = Follow.objects.filter(user__username=user.username)
        return new_queryset

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
