from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('registration/', views.RegisterFormView.as_view(),name='registration'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('story_list/', views.story_list, name='story_list'),
    path('story_list/story/<int:pk>/', views.story_detail, name='story_detail'),

]
