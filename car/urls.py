from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('accounts/registration/', views.RegisterFormView.as_view(), name='registration'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('story_list/', views.story_list, name='story_list'),
    path('story_list/story/<int:pk>/', views.story_detail, name='story_detail'),
    path('story_add/', views.story_add, name='story_add'),
    path('story_continue/', views.story_continue, name='story_continue'),
    path('statistics/', views.statistics, name='statistics')
]
