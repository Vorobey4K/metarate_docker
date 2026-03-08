from django.contrib import admin,messages
from django.utils.safestring import mark_safe
from slugify import slugify
from .models import Creator,Movie,Genre,Book,Series,ComputerGame
# Register your models here.

admin.site.site_header = "MetaRate Admin"
admin.site.site_title = "MetaRate Management"
admin.site.index_title = "Панель управления контентом"

def update_field_values(queryset, field, value):
    """
    Обновляет указанное поле у всех объектов в queryset, если значение отличается.
    Возвращает количество обновлённых записей.
    """
    updated_count = 0
    for obj in queryset:
        if getattr(obj, field) != value:
            setattr(obj, field, value)
            obj.save()
            updated_count += 1
    return updated_count

class FilterTypeGenre(admin.SimpleListFilter):
    title = 'Тип контента'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        queryset_genre = Genre.objects.filter(content_type=model_admin.content_type)
        return [(query.slug,query.name) for query in queryset_genre]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(genres__slug=self.value())
        return  queryset

class BaseMediaAdmin(admin.ModelAdmin):

    content_type = None

    fields = ['title','creator','year','rating','country','post_photo','poster','genres',
                'description','full_description','page_author']
    list_display = ('id', 'title','rating','post_photo','year','creator')
    list_display_links = ('id', 'title')
    ordering = ['-rating','title']
    list_per_page = 10
    actions = ['assign_page_author']
    search_fields =['title__istartswith','=year']
    list_filter = [FilterTypeGenre]
    filter_horizontal = ('genres',)
    readonly_fields = ('post_photo',)
    save_on_top = True



    @admin.display(description='Изображение')
    def post_photo(self,media):
        return mark_safe(f'<img src={media.poster.url} width=60')


    @admin.action(description='Назначить текущего пользователя автором')
    def assign_page_author(self,request,queryset):

        count = update_field_values(queryset=queryset, field='page_author', value=request.user)
        self.message_user(request,f'Автор назначен для {count} записей')

@admin.register(Series)
class SeriesAdmin(BaseMediaAdmin):
    content_type  = 'Фильм'

@admin.register(Book)
class BookAdmin(BaseMediaAdmin):
    content_type  = 'Книга'


@admin.register(ComputerGame)
class ComputerGameAdmin(BaseMediaAdmin):
    content_type = 'Игра'
    fields = BaseMediaAdmin.fields + ['budget']

@admin.register(Movie)
class MovieAdmin(BaseMediaAdmin):
    content_type  = 'Фильм'
    fields = BaseMediaAdmin.fields + ['budget']

@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    fields = ['name','type']
    list_display = ('id', 'name','type')
    list_display_links = ('id', 'name')
    ordering = ['id']
    list_per_page = 20
    search_fields = ['name__istartswith']
    list_filter = ['type']
    actions = ['set_type_to_studio','set_type_to_author','set_type_to_director']
    save_on_top = True

    @admin.action(description='Сменить тип на Студия')
    def set_type_to_studio(self, request, queryset):
        count = update_field_values(queryset, 'type', 'studio')
        self.message_user(request, f'Тип обновлён на "Студия" для {count} записей.')

    @admin.action(description='Сменить тип на Автор')
    def set_type_to_author(self, request, queryset):
        count = update_field_values(queryset, 'type', 'author')
        self.message_user(request, f'Тип обновлён на "Автор" для {count} записей.')

    @admin.action(description='Сменить тип на Директор')
    def set_type_to_director(self, request, queryset):
        count = update_field_values(queryset, 'type', 'director')
        self.message_user(request, f'Тип обновлён на "Директор" для {count} записей.')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['name', 'content_type']
    list_display = ('id', 'name', 'content_type')
    list_display_links = ('id', 'name')
    ordering = ['id']
    list_per_page = 20
    search_fields = ['name__istartswith']
    list_filter = ['content_type']
    actions = ['set_content_type_film', 'set_content_type_book', 'set_content_type_game']
    save_on_top = True

    @admin.action(description='Сменить тип на Фильм')
    def set_content_type_film(self, request, queryset):
        count = update_field_values(queryset, 'content_type', 'movie')
        self.message_user(request, f'Content type обновлён на "Фильм" для {count} записей.')

    @admin.action(description='Сменить тип на Книга')
    def set_content_type_book(self, request, queryset):
        count = update_field_values(queryset, 'content_type', 'book')
        self.message_user(request, f'Content type обновлён на "Книга" для {count} записей.')

    @admin.action(description='Сменить тип на Игра')
    def set_content_type_game(self, request, queryset):
        count = update_field_values(queryset, 'content_type', 'game')
        self.message_user(request, f'Content type обновлён на "Игра" для {count} записей.')