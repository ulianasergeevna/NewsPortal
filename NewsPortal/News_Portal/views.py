from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from .models import Post
from .filters import PostFilter


class PostList(ListView):
    model = Post
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    ordering = ['publication_time']
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS).order_by('-publication_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'