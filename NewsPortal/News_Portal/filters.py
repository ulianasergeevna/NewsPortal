from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post
        #fields = ('publication_time', 'heading', 'author', 'categories__in')
        fields = {
            'publication_time': ['gt'],
            'heading': ['contains'],
            'author': ['exact'],
            'categories__name': ['in']
        }
