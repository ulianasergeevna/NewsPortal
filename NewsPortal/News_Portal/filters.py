from django_filters import FilterSet
from .models import Post
from django.core.paginator import Paginator
from datetime import datetime as dt


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'heading': ['contains'],
            'author': ['exact'],
            'categories__name': ['in']
        }

    @property
    def qs(self):
        qs = super().qs
        date_search = self.data.get('date_search')
        if date_search:
            qs = qs.filter(publication_time__gt=dt.fromisoformat(date_search))
        return qs
