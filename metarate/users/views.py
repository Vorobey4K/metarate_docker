

from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from catalog.models import MediaItem
from interactions.models import UserMediaStatus, Review

from .forms import LoginFormUser, RegisterFormUser,  UpdateProfileUserForm

from .services.profile import filter_main,filter_by_sorting,filter_by_content_type,completed_counts

from .models import Profile

class LoginUser(LoginView):
    form_class = LoginFormUser
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    extra_context = {'title': 'Вход в аккаунт','title_button': 'Войти'}

class RegisterUser(CreateView):
    form_class = RegisterFormUser
    success_url = reverse_lazy('users:login')
    template_name = 'universal_form.html'
    extra_context = {'title': "Регистрация", 'title_button': 'Зарегистрироваться'}


@login_required
def profile(request):
    x = 0
    user = request.user
    tab = request.GET.get('tab', 'completed')
    type_content = request.GET.get('type_content', '')
    sort = request.GET.get('sort', 'rating')

    items = filter_main(tab, user)


    if sort:
        items = filter_by_sorting(items, sort)

    content_type = request.GET.get('type_content')
    if content_type:
        items = filter_by_content_type(items, content_type)

    return render(
        request,
        'users/profile.html',
        {
            'items': items,
            'tab': tab,
            'type_content':type_content,
            'sort':sort,
            'completed_counts':completed_counts(user)
        }
    )

class UpdateProfileUser(LoginRequiredMixin,UpdateView):
    form_class = UpdateProfileUserForm
    template_name = 'universal_form.html'
    extra_context = {'title': "Профиль рецензию", 'title_button': 'Сохранить'}
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return Profile.objects.get(user_id=self.request.user.id)

    def form_valid(self, form):
        profile = form.save(commit=False)
        user = profile.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        profile.save()
        return super().form_valid(form)

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users:login'))