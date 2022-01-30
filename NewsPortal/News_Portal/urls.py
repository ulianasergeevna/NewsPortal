from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('search', PostSearch.as_view()),
    path('add', PostCreate.as_view()),
    path('<int:pk>/edit', PostUpdate.as_view()),
    path('<int:pk>/delete', PostDelete.as_view()),
]