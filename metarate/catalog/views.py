from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy,reverse

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView

from interactions.models import UserMediaStatus
from .models import Movie, Book, Series, ComputerGame

from users.services.profile import filter_by_sorting

class HomePageView(TemplateView):
    template_name = 'catalog/home.html'

class BaseList(ListView):
    template_name = 'catalog/content_list.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')

        sort = self.request.GET.get('sort')
        if sort:
            queryset = filter_by_sorting(
                queryset=queryset,
                type_sort=sort
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort','')
        return context




class MovieList(BaseList):
    model = Movie
    extra_context = {'title':'Список фильмов'}


class BookList(BaseList):
    model = Book
    extra_context = {'title':'Список Книг'}



class SeriesList(BaseList):
    model = Series
    extra_context = {'title':'Список сериалов'}



class GameList(BaseList):
    model = ComputerGame
    extra_context = {'title':'Список игр'}



class BaseMediaPost(LoginRequiredMixin,DetailView):
    template_name = 'catalog/content_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        record = UserMediaStatus.objects.filter(user=self.request.user, mediaitem=self.object)
        if record:
            context['media_status'] = record[0]
        return context


class MoviePost(BaseMediaPost):
    model = Movie
    extra_context = {'planned': 'Буду смотреть',
        'completed': 'Просмотрен',}

class BookPost(BaseMediaPost):
    model = Book
    extra_context = {'planned': 'Буду читать',
        'completed': 'Прочитан'}
class SeriesPost(BaseMediaPost):
    model = Series
    extra_context = {'planned': 'Буду смотреть',
                    'completed': 'Просмотрен', }

class GamePost(BaseMediaPost):
    model = ComputerGame
    extra_context = {'planned': 'Буду играть',
                    'completed': 'Пройден'}




# class MovieAdd(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
#     form_class = MovieForm
#     template_name = 'catalog/movie_add.html'
#     success_url = reverse_lazy('movie_list')
#     extra_context = {'title':'Добавить фильм'}
#     permission_required = 'catalog.add_movie'
#
#
#
#     def form_valid(self, form):
#         p = form.save(commit=False)
#         p.page_author = self.request.user
#         p.save()
#         return super().form_valid(form)
#
#
# class MovieUpdate(LoginRequiredMixin,UpdateView):
#     model = Movie
#     form_class = MovieForm
#     template_name = 'catalog/movie_update.html'
#     extra_context = {'title':'Изменить фильм'}
#     success_url = reverse_lazy('movie_list')
#
#
# class MovieDelete(LoginRequiredMixin,DeleteView):
#     model = Movie
#     template_name = 'catalog/movie_delete.html'
#     extra_context = {'title':'Изменить фильм'}
#     success_url = reverse_lazy('movie_list')


# class CreatorAdd(LoginRequiredMixin,CreateView):
#     form_class = CreatorForm
#     template_name = 'catalog/movie_add.html'
#     success_url = reverse_lazy('movie_list')
#     extra_context = {'title':'Добавить Директора'}
#
