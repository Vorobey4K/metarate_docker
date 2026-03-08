
from django.urls import path
from .views import MovieList, MoviePost, HomePageView, GameList, SeriesList, \
    BookList, BookPost, SeriesPost, GamePost

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),

    path('movie-list',MovieList.as_view(),name='movie_list'),
    path('game-list',GameList.as_view(),name='game_list'),
    path('series-list',SeriesList.as_view(),name='series_list'),
    path('book_list',BookList.as_view(),name='book_list'),

    path('movie/<slug:slug>',MoviePost.as_view(),name='movie_detail'),
    path('book/<slug:slug>',BookPost.as_view(),name='book_detail'),
    path('series/<slug:slug>',SeriesPost.as_view(),name='series_detail'),
    path('game/<slug:slug>',GamePost.as_view(),name='game_detail'),

]

