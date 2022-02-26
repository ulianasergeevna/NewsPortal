from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from NewsPortal.forms import ProfileUpdateForm


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...


def login_form(request):
    return render(request, 'login_form.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'edit_profile_form.html'
    form_class = ProfileUpdateForm
    success_url = '/profile/'

    def get_object(self, **kwargs):
        return self.request.user


class IndexView(TemplateView):
    template_name = 'index.html'

