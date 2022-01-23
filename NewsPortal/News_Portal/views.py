from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from .models import Post, Author
from .filters import PostFilter


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete_post_form.html'
    success_url = '/news'
    context_object_name = 'news'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostCreate(CreateView):
    model = Post
    template_name = 'create_post_form.html'
    fields = ['author', 'categories', 'heading', 'post_type', 'text']


class PostUpdate(UpdateView):
    model = Post
    template_name = 'create_post_form.html'
    fields = ['author', 'categories', 'heading', 'post_type', 'text']

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostList(ListView):
    model = Post
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    ordering = ['-publication_time']
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS).order_by('-publication_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=Post.objects.filter(post_type='NW'))
        return context

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер

        author = Author.objects.get(pk=int(request.POST['author']))
        post_type = request.POST['post_type']
        category_ids = request.POST['categories']
        heading = request.POST['heading']
        text = request.POST['text']

        post = Post(author=author, post_type=post_type, heading=heading, text=text)  # создаём новый товар и сохраняем
        post.save()

        for cid in category_ids:
            post.categories.set(cid)

        return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        post.update(**kwargs)
        return super().put(request, *args, **kwargs)


class PostSearch(ListView):
    model = Post
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    ordering = ['-publication_time']
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='NW').order_by('-publication_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET,
            queryset=self.get_queryset())

        return context