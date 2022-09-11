from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from achievements.views import add_base_achivement, get_user_achievments
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
            return redirect("main")
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


@login_required
def user_profile(request):
    """Вывод страницы пользователя"""
    users_idea_liked = UserIdeaLike.objects.filter(user=request.user)
    list_user_idea = Idea.objects.filter(user=request.user)
    # Получение решений для идей пользователя
    solution_list = Solution.objects.filter(idea__user=request.user)
    # Получение достижений пользователя
    user_achievments = get_user_achievments(request.user)
    context = {
        "users_idea_liked": users_idea_liked,
        "list_user_idea": list_user_idea,
        "solution_list": solution_list,
        "user_achievments":user_achievments,
    }
    return render(request, "registration/profile.html", context)


@login_required
def change_user(request):
    """Изменение страницы пользователя"""
    user_form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        avatar = request.POST.get("avatar")
        print(avatar)
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user-profile')
    context = {
        "user_form": user_form,
    }
    return render(request, "registration/change_profile.html", context)


# Главное меню
def main(request):
    context = {}
    return render(request, "main.html", context)


# Странциа с банкой
def get_idea_title(request):
    """Вывод страницы идей"""
    idea_list = Idea.objects.all()
    idea_tag_list = IdeaTags.objects.all()
    context = {
        "idea_list": idea_list,
        "idea_tag_list": idea_tag_list
    }
    return render(request, "ideas/get_idea_random.html", context)


# Получение значений на странице с банкой
def filter_idea_random(request):
    """Фильтрация идей и вывод по 1"""
    check = []
    idea_list = Idea.objects.exclude(user=request.user)

    # Получение идей пользователя, которые он отметил
    users_checked_idea = UserIdeaLike.objects.filter(user=request.user).filter(
        checked_idea=True)  # последний фильтр под вопросом
    idea_tag_list = IdeaTags.objects.all()

    # Получаем теги из формы
    for tag in idea_tag_list:
        check.append(request.GET.get(tag.name))

    # Фильтруем по тегам
    for tag in check:
        if tag is not None:
            idea_list = idea_list.filter(
                Q(tags__name=tag)
            )
    # Фильтруем по отмеченным идеям
    for checked_idea in users_checked_idea:
        idea_list = idea_list.exclude(id=checked_idea.idea.id)

    # Получение случайной
    new_idea = idea_list.order_by('?').first()
    context = {
        "idea_list": idea_list,
        "idea_tag_list": idea_tag_list,
        "new_idea": new_idea,
    }
    return render(request, "ideas/get_idea_random.html", context)


def like_idea(request, pk):
    """Добавление идей в избранное"""
    user = request.user
    idea_user_author = Idea.objects.get(id=pk)
    author = User.objects.get(id=idea_user_author.user.id)
    print(pk)
    UserIdeaLike.objects.create(idea_id=pk, user=user, checked_idea=True)
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
    delete_idea.delete()
    if user.rating >= 10:
        user.rating -= 10
        user.save()
    return redirect('user-profile')


# def filter_idea(request):
#     check = []
#     idea_list = Idea.objects.all()
#     idea_tag_list = IdeaTags.objects.all()
#     for tag in idea_tag_list:
#         check.append(request.GET.get(tag.name))
#     for tag in check:
#         if tag is not None:
#             idea_list = idea_list.filter(
#                 Q(tags__name=tag)
#             )
#     context = {
#         "idea_list": idea_list,
#         "idea_tag_list": idea_tag_list
#     }
#     return render(request, "ideas/get_idea_random.html", context)


# Создание новой идеи
def create_idea(request):
    tags_idea = IdeaTags.objects.all()
    form = IdeaForm()
    user = request.user
    if request.method == 'POST':
        form = IdeaForm(request.POST)

        ###
        tags_names = [x.name for x in tags_idea]
        tags_ids = []
        for x in tags_names:
            tags_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print()
            print(tags_ids)
        ###
        if form.is_valid():
            obj = form.save(commit=False)
            # Добавление пользователя к записи если авторизован
            if user.is_authenticated:
                obj.user = user
            obj.save()
            print(obj.user)
            for x in tags_ids:
                obj.tags.add(IdeaTags.objects.get(id=x))
            obj.save()
            # Тестовое достижение
            add_base_achivement(user, name="Первый шаг")

            return redirect("user-profile")
        else:
            print(form.errors)
    context = {
        "form": form,
        "tags_idea": tags_idea,
    }
    return render(request, "ideas/create_new_idea.html", context)


# Изменение идеи пользователя
def update_user_idea(request, pk):
    tags_idea = IdeaTags.objects.all()
    idea = Idea.objects.get(id=pk)
    form = IdeaForm(instance=idea)
    tags_idea_current = IdeaTags.objects.filter(ideas__id=pk)

    if request.method == "POST":
        form = IdeaForm(request.POST, instance=idea)

        tags_names = [x.name for x in tags_idea]
        tags_ids = []
        for x in tags_names:
            tags_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print()
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
        "tags_idea": tags_idea,
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


def add_solution_to_idea(request, pk):
    idea_to_solution = UserIdeaLike.objects.get(id=pk)
    form = SolutionForm(instance=idea_to_solution)
    if request.method == "POST":
        form = SolutionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
        else:
            print(form.errors)
    context ={
        "idea": idea_to_solution,
        "form": form
    }
    return render(request, "ideas/add_solution.html", context)

