from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'newslist.html'
    context_object_name = 'newslist'

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS).order_by('publication_time')


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'