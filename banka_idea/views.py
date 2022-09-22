from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.core.cache import cache

from achievements.views import add_base_achivement, add_achievments_to_user, get_user_achievments_unlocked, \
    get_user_achievments_locked
from banka_idea.forms import CustomUserCreationForm, IdeaForm, UpdateUserForm, SolutionForm
from banka_idea.models import Idea, IdeaTags, UserIdeaLike, User, Solution


### Пользователь

# Регистрация
class Register(View):
    template_name = "registration/register.html"

    def get(self, request):
        context = {
            "form": CustomUserCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            add_achievments_to_user(user)
            return redirect("main")
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


@login_required
def user_profile(request):
    """Вывод страницы пользователя"""
    users_idea_liked_not_finish = UserIdeaLike.objects.filter(user=request.user).filter(checked_idea=False).order_by(
        "date")
    users_idea_liked_finish = UserIdeaLike.objects.filter(user=request.user).filter(checked_idea=True).order_by("date")
    list_user_idea = Idea.objects.filter(user=request.user).order_by("date")
    # Получение решений для идей пользователя
    solution_list = Solution.objects.filter(idea__user=request.user).order_by("date").order_by("-best_solution")
    users_solution = Solution.objects.filter(user=request.user).order_by("date")
    # Получение достижений пользователя
    user_achievments = get_user_achievments_unlocked(request.user)
    context = {
        "users_idea_liked": users_idea_liked_not_finish,
        "users_idea_liked_finish": users_idea_liked_finish,
        "list_user_idea": list_user_idea,
        "solution_list": solution_list,
        "user_achievments": user_achievments,
        "users_solution": users_solution,
    }
    return render(request, "registration/profile.html", context)


@login_required
def change_user(request):
    """Изменение страницы пользователя"""
    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user-profile')
    context = {
        "user_form": user_form,
    }
    return render(request, "registration/change_profile.html", context)


### Главное меню
def main(request):
    context = {}
    return render(request, "main.html", context)


def about_page(request):
    context = {}
    return render(request, "about.html", context)


# Странциа с банкой
def get_idea_random_title(request):
    """Вывод страницы банки"""
    idea_list = Idea.objects.all()
    idea_tag_list = IdeaTags.objects.all().order_by('name')
    context = {
        "idea_list": idea_list,
        "idea_tag_list": idea_tag_list
    }
    return render(request, "ideas/get_idea_random.html", context)


def get_idea_list_title(request):
    """Вывод страницы списка"""
    idea_tag_list = IdeaTags.objects.all().order_by('name')
    # Получение идей пользователя, которые он отметил
    if request.user.is_authenticated:
        idea_list = Idea.objects.exclude(user=request.user)
        users_checked_idea = UserIdeaLike.objects.filter(user=request.user)  # последний фильтр под вопросом
        users_idea = UserIdeaLike.objects.filter(user=request.user)
        for checked_idea in users_checked_idea:
            idea_list = idea_list.exclude(id=checked_idea.idea.id)
    else:
        idea_list = Idea.objects.all().order_by('date')
    print(users_idea)
    print(idea_list)
    context = {
        "idea_list": idea_list,
        "idea_tag_list": idea_tag_list
    }
    return render(request, "ideas/get_idea_list.html", context)


def get_list_idea_filter(request):
    """Фильтры для страницы списка идей"""
    idea_tag_list = IdeaTags.objects.all().order_by('name')
    check = []
    if request.user.is_authenticated:
        idea_list = Idea.objects.exclude(user=request.user).order_by('date')
    else:
        idea_list = Idea.objects.all().order_by('date')

    # Получаем теги из формы
    for tag in idea_tag_list:
        check.append(request.GET.get(tag.name))
    print(check)
    # Фильтруем по тегам
    for tag in check:
        if tag is not None:
            idea_list = idea_list.filter(
                Q(tags__id=tag)
            )
    if not idea_list:
        return redirect('main')
    context = {
        "idea_list": idea_list,
        "idea_tag_list": idea_tag_list,
    }
    return render(request, "ideas/get_idea_list.html", context)


# Получение значений на странице с банкой
def filter_idea_random(request):
    """Фильтрация идей и вывод по 1"""
    check = []
    idea_list = Idea.objects.exclude(user=request.user)
    cache.delete('idea_list')
    cache.delete('new_idea')

    # Получение идей пользователя, которые он отметил
    users_checked_idea = UserIdeaLike.objects.filter(user=request.user)  # последний фильтр под вопросом
    idea_tag_list = IdeaTags.objects.all()
    print("Список идей", idea_list)

    # Получаем теги из формы
    for tag in idea_tag_list:
        check.append(request.GET.get(tag.name))
    print("Теги", check)
    # Фильтруем по тегам
    for tag in check:
        if tag is not None:
            idea_list = idea_list.filter(
                Q(tags__id=tag)
            )

    # Фильтруем по отмеченным идеям
    for checked_idea in users_checked_idea:
        idea_list = idea_list.exclude(id=checked_idea.idea.id)
    print("Новый список идей", idea_list)

    # Получение случайной
    new_idea = idea_list.order_by('?').first()
    print(new_idea)
    if not idea_list:
        return redirect('main')

    cache.set('idea_list', idea_list)
    context = {
        "idea_list": idea_list,
        "idea_tag_list": idea_tag_list,
        "new_idea": new_idea,
    }
    return render(request, "ideas/idea_cookie.html", context)


def delete_idea_random(request, pk):
    idea_list = cache.get('idea_list')
    ban_list = cache.set('new_idea', pk)
    ban_list_get = cache.get('new_idea')
    print("Список готовых идей", idea_list)
    print("Список идей для бана", ban_list_get)
    if len(idea_list) > 1:
        idea_list = idea_list.exclude(id=ban_list_get)
        print("Измененный", idea_list)
        cache.set('idea_list', idea_list)
        new_idea = idea_list.order_by('?').first()
    else:
        return redirect('main')
    context = {
        "new_idea": new_idea,
    }
    return render(request, "ideas/idea_cookie.html", context)


def like_idea(request, pk):
    """Добавление идей в избранное"""
    user = request.user
    # Получение автора идеи
    idea = Idea.objects.get(id=pk)
    author = User.objects.get(id=idea.user.id)
    # Добавление в лайк
    UserIdeaLike.objects.create(idea_id=pk, user=user, checked_idea=False)
    author.rating += 10
    author.save()
    messages.success(request, 'Идея добавлена в избранное')
    context = {

    }
    return render(request, "main.html", context)


def dislike_idea(request, pk):
    """Удаление идей из избранного"""
    print(pk)
    user = User.objects.get(id=request.user.id)
    delete_idea = UserIdeaLike.objects.get(id=pk)

    if delete_idea.checked_idea:
        delete_idea.checked_idea = False
        delete_idea.save()
    else:
        delete_idea.delete()
    if user.rating >= 10:
        user.rating -= 10
        user.save()
    return redirect('user-profile')


# Создание новой идеи
def create_idea(request):
    idea_tag_list = IdeaTags.objects.all().order_by('name')
    form = IdeaForm()
    user = request.user
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        ###
        tags_names = [x.name for x in idea_tag_list]
        tags_ids = []
        for x in tags_names:
            if request.POST.get(x):
                tags_ids.append(int(request.POST.get(x)))
        ###
        if form.is_valid():
            obj = form.save(commit=False)
            # Добавление пользователя к записи если авторизован
            if user.is_authenticated:
                obj.user = user
            obj.save()
            for x in tags_ids:
                obj.tags.add(IdeaTags.objects.get(id=x))
            obj.save()
            user.rating += 5
            user.save()

            # Тестовое достижение
            add_base_achivement(user, name="Первый шаг")

            return redirect("user-profile")
        else:
            print(form.errors)
    context = {
        "form": form,
        "tags_idea": idea_tag_list,
    }
    return render(request, "ideas/create_new_idea.html", context)


# Изменение идеи пользователя
def update_user_idea(request, pk):
    idea_tag_list = IdeaTags.objects.all().order_by('name')
    idea = Idea.objects.get(id=pk)
    form = IdeaForm(instance=idea)
    tags_idea_current = IdeaTags.objects.filter(ideas__id=pk)

    if request.method == "POST":
        form = IdeaForm(request.POST, instance=idea)

        tags_names = [x.name for x in idea_tag_list]
        tags_ids = []
        for x in tags_names:
            if request.POST.get(x):
                tags_ids.append(int(request.POST.get(x)))
            print(tags_ids)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.tags.clear()
            obj.save()
            for x in tags_ids:
                obj.tags.add(IdeaTags.objects.get(id=x))
            obj.save()
            return redirect('user-profile')
    context = {
        "tags_idea": idea_tag_list,
        "tags_idea_current": tags_idea_current,
        "idea": idea,
        "form": form
    }
    return render(request, "ideas/change_idea.html", context)


# Удаление идеи пользователя
@login_required
def delete_user_idea(request, pk):
    idea = Idea.objects.get(id=pk)
    idea.delete()
    return redirect("user-profile")


# Добавление ответа к идее
def add_solution_to_idea(request, pk):
    idea_to_solution = UserIdeaLike.objects.get(id=pk)
    form = SolutionForm(instance=idea_to_solution)
    idea_finish = UserIdeaLike.objects.get(idea__id=idea_to_solution.idea.id)
    if request.method == "POST":
        form = SolutionForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            # print(form)
            form.save()
            idea_finish.checked_idea = True
            idea_finish.save()
            return redirect('user-profile')
        else:
            print(form.errors)
    context = {
        "idea": idea_to_solution,
        "form": form
    }
    return render(request, "solutions/add_solution.html", context)


# Изменение ответа к идее
def solution_update(request, pk):
    solution = Solution.objects.get(id=pk)
    form = SolutionForm(instance=solution)
    if request.method == "POST":
        form = SolutionForm(request.POST, request.FILES, instance=solution)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('user-profile')
        else:
            print(form.errors)
    context = {
        "form": form,
        "solution": solution
    }
    return render(request, "solutions/update_solution.html", context)


# Изменение ответа к идее
def solution_delete(request, pk):
    solution = Solution.objects.get(id=pk)
    # Проверка на пользователя
    if request.user == solution.user:
        solution.delete()
    return redirect("user-profile")


# Поиск
def search_results(request):
    query = request.GET.get('search')
    object_list = Idea.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    users_ideas = Idea.objects. \
        filter(useridealike__user=request.user).filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    context = {
        "object_list": object_list,
        "users_ideas": users_ideas,
        "query": query,
    }
    return render(request, 'ideas/search_results.html', context)


def tags_search(request, pk):
    query = IdeaTags.objects.get(id=pk)
    object_list = Idea.objects.filter(tags__in=[query])
    users_ideas = Idea.objects.filter(useridealike__user=request.user).filter(tags__in=[query])
    print("Запрос по тегам", object_list)
    context = {
        "query": query,
        "object_list": object_list,
        "users_ideas": users_ideas,
    }
    return render(request, 'ideas/search_results.html', context)


def set_best_solution(request, pk):

    solution = Solution.objects.get(id=pk)
    ideas_in_solution = Solution.objects.filter(idea__user=request.user).filter(idea=solution.idea)
    for idea in ideas_in_solution:
        idea.best_solution = False
        idea.save()
    solution.best_solution = True
    solution.save()

    return redirect("user-profile")