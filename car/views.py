from django.shortcuts import render, get_object_or_404, redirect
from .models import Story
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from .forms import StoryForm
from .forms import StoryAddForm

# Create your views here.
def homepage(request):
    return render(request, 'car/homepage.html',{})


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "car/login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "car/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

def story_list(request):
    storys = Story.objects.filter(contributors=request.user, finished=True)
    return render(request, 'car/story_list.html', {'storys': storys})


def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    return render(request, 'car/story_detail.html', {'story': story})

def story_add(request):
    if request.method == "POST":
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.save()
            story.contributors.add(request.user)
            story.finished = False
            story.text = story.last_added_text
            story.first_added_text_or_name=story.last_added_text
            story.save()
            return redirect('homepage')
    else:
        form = StoryForm()
    return render(request, 'car/story_add.html', {'form':form})

def story_continue(request):
    story_rand = Story.objects.filter(finished=False).order_by("?").first()

    if request.method == "POST":
        form = StoryAddForm(request.POST, instance=story_rand)
        if form.is_valid():
            story = form.save(commit=False)
            story.contributors.add(request.user)
            story.text = story.text + "/n" + story.last_added_text

            if (story.contributors.count()<=1):
                story.finished=False
            else:
                story.finished = story.finished

            story.save()
            return redirect('homepage')
    else:
        form = StoryAddForm()
    return render(request, 'car/story_continue.html', {'form':form , 'story_rand':story_rand})


