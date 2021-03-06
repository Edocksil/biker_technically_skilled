from django.shortcuts import render, get_object_or_404, redirect
from .models import Story
from django.utils import timezone
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import StoryForm, StoryAddForm
from django.db.models import Count


# Create your views here.
def homepage(request):
    return render(request, 'car/homepage.html', {})

# used DJANGO implementation for login(out) instead of it:
""" 
class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "registration/login.html"

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
"""

class RegisterFormView(FormView):
    form_class = UserCreationForm
    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/register.html"
    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/accounts/login/"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

def story_list(request):
    try:
        if (User.is_authenticated):
            stories = Story.objects.filter(contributors=request.user, finished=True)
            if stories.count() == 0:
                return render(request, 'story/no_storys_left.html')
            else:
                return render(request, 'story/story_list.html', {'stories': stories})
        else:
            render(request, '', {})
    except TypeError:
        return render(request, 'car/homepage.html')

def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    return render(request, 'story/story_detail.html', {'story': story})

def story_add(request):
    try:
        storys = Story.objects.filter(contributors=request.user)
    except TypeError:
        return render(request, 'car/homepage.html')
    if request.method == "POST":
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.save()
            story.contributors.add(request.user)
            story.finished = False
            story.text = story.last_added_text
            story.first_added_text_or_name=story.last_added_text
            story.count = 1
            story.last = request.user.username
            story.save()
            return redirect('homepage')
    else:
        form = StoryForm()
    return render(request, 'story/story_add.html', {'form': form})

def story_continue(request):
    try:
        storys = Story.objects.filter(contributors=request.user)
    except TypeError:
        return render(request, 'car/homepage.html')
    story_rand = ''
    last_user = ''
    x = True
    retries = 0
    try:
        while(x):
            retries += 1
            story_rand = Story.objects.filter(finished=False).order_by("?").first()
            last_user= story_rand.last
            if (last_user!= User.get_username(request.user)):
                x = False
            if (retries > 100):
                raise ZeroDivisionError('no stories for you')
    except AttributeError:
        return render(request, 'story/no_storys_left.html')
    except ZeroDivisionError:
        return render(request, 'story/no_storys_left.html')

    if story_rand.count<10:
        StoryFormVar = StoryForm(request.POST, instance=story_rand)
    else:
        StoryFormVar = StoryAddForm(request.POST, instance=story_rand)

    if request.method == "POST":
        form = StoryFormVar
        if form.is_valid():
            story = form.save(commit=False)
            story.contributors.add(request.user)
            story.text = story.text + "\n" + story.last_added_text
            story.last = request.user.username
            if (story.count<10):
                story.finished = False

            story.finished = story.finished
            story.count += 1
            story.save()
            return redirect('homepage')
    else:
        form = StoryFormVar
    return render(request, 'story/story_continue.html', {'form': form, 'story_rand': story_rand, 'last_user': last_user})

class Stat:
    def __init__(self, name):
        self.name = name
        self.finished_stories=Story.objects.filter(finished=True).count()
        self.unfinished_stories=Story.objects.filter(finished=False).count()
        self.total_stories=Story.objects.count()

        self.best_contributor=Story.objects.values('contributors').annotate(dcontributor=Count('contributors')).order_by('-dcontributor').first()
        self.best_count=self.best_contributor.get('dcontributor')
        self.best_user=User.objects.filter(id=self.best_contributor['contributors']).values('username').get()


        self.worst_contributor=Story.objects.values('contributors').annotate(dcontributor=Count('contributors')).order_by('dcontributor').first()
        self.worst_count=self.worst_contributor.get('dcontributor')
        self.worst_user=User.objects.filter(id=self.worst_contributor['contributors']).values('username').get()

        self.test = Story.objects.values('count').annotate(dcount=Count('count'))

def statistics(request):
    try:
        storys = Story.objects.filter(contributors=request.user)
    except TypeError:
        return render(request, 'car/homepage.html')

    full_statistic=Stat('Stat_object')
    return render(request, 'car/statistics.html', {'full_statistic': full_statistic})




