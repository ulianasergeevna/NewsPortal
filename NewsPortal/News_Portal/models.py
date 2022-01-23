from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        postcommentRat = self.post_set.comment_set.aggregate(postcommentRating=Sum('rating'))
        pcRat = 0
        pcRat += postcommentRat.get('postcommentRating')

        self.rating = pRat * 3 + cRat + pcRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name='Автор')

    ARTICLE = 'AR'
    NEWS = 'NW'

    TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'новость'),
    ]

    post_type = models.CharField(max_length=2,
                                 choices=TYPES,
                                 default=ARTICLE)

    publication_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    categories = models.ManyToManyField('Category', through='PostCategory', verbose_name='Категория')
    heading = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def get_absolute_url(self):
        return f'/news/{self.pk}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
