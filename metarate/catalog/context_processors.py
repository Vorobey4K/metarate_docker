# context = {'movie_list':'Cписок фильмов',
#            'penis':'Авторизация'}


def get_navigation(request):
    return {'navigation':{'movie_list':'Cписок фильмов','login':'Авторизация','profile':'Профиль'}}