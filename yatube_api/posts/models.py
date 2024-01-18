from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

LIMIT = 20


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title[:LIMIT]


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:LIMIT]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.post} - {self.author}'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            ),
            models.CheckConstraint(
                check=~models.Q(models.F('user') == models.F('following')),
                name='user_not_following'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.following}'
