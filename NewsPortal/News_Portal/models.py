from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)
    # допустим, очень активный автор, который всех бесит,
    # постит по паре-тройке статей и паре десятков комментов в день,
    # каждый из которых сu1 = User.objects.get(username='ChtoNibut')
    #
    # u2 = User.objects.get(username='User_4')табильно огребает по мешку дизлайков.
    # Как быстро его антирейтинг перерастёт SmallIntegerField,
    # если вариант "забанить" недоступен?

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
    name = models.CharField(max_length=64,
                                unique=True)


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    ARTICLE = 'AR'
    NEWS = 'NW'

    TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'новость'),
    ]

    post_type = models.CharField(max_length=2,
                                 choices=TYPES,
                                 default=ARTICLE)

    publication_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

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
