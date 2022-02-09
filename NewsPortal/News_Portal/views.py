import view as view
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator
from .models import Post, Author
from .filters import PostFilter
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    ordering = ['-publication_time']
    paginate_by = 10

    def get_initial_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS).order_by('-publication_time')

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=self.get_initial_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = {**super().get_context_data(**kwargs), 'filter': self.get_filter()}
        context['date_search'] = context['filter'].data.get('date_search')
        return context

    def post(self, request, *args, **kwargs):
        author = Author.objects.get(pk=int(request.POST['author']))
        post_type = request.POST['post_type']
        category_ids = request.POST['categories']
        heading = request.POST['heading']
        text = request.POST['text']

        post = Post(author=author, post_type=post_type, heading=heading, text=text)
        post.save()

        for cid in category_ids:
            post.categories.set(cid)

        return super().get(request, *args, **kwargs)


class PostSearch(View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, 'search.html', context)

    def get_initial_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS).order_by('-publication_time')

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=self.get_initial_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            'filter': self.get_filter(),
        }


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        post.update(**kwargs)
        return super().put(request, *args, **kwargs)


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News_Portal.add_post',)
    model = Post
    template_name = 'create_post_form.html'
    fields = ['author', 'categories', 'heading', 'post_type', 'text']


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News_Portal.change_post',)
    model = Post
    template_name = 'create_post_form.html'
    fields = ['author', 'categories', 'heading', 'post_type', 'text']

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News_Portal.delete_post',)
    model = Post
    template_name = 'delete_post_form.html'
    success_url = '/news'
    context_object_name = 'news'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
