from django.contrib import admin
from django.contrib.admin import action
from django.utils.safestring import mark_safe

from interactions.models import Review,UserMediaStatus

# Register your models here.
class MediaTypeFilter(admin.SimpleListFilter):
    title = 'Тип контента'
    parameter_name = 'content_type'

    def lookups(self, request, model_admin):

        return [
            ('movie','Фильмы'),
            ('series','Сериалы'),
            ('book','Книги'),
            ('computergame','Игры')
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(mediaitem__content_type=self.value())
        return queryset


class BaseAdminInteractions(admin.ModelAdmin):
    list_per_page = 10
    @admin.display(description='Изображение')
    def post_photo(self, obj):
        return mark_safe(f'<img src={obj.mediaitem.poster.url} width=60')

    @admin.display(description='Заголовок медиа')
    def title_media(self, obj):
        return obj.mediaitem.title

    @admin.display(description='Имя пользователя')
    def user_name(self, obj):
        return obj.user.username

@admin.register(Review)
class AdminReview(BaseAdminInteractions):
    fields = ['title','text','rating','sentiment','user_name','title_media','created_at']
    readonly_fields = ('sentiment','title_media','created_at','user_name')
    list_display = ('id','title','title_media','post_photo','rating','user_name','created_at')
    list_display_links = ('id','title')
    list_filter = [MediaTypeFilter,'sentiment']
    ordering = ['-created_at','title']
    search_fields = ['mediaitem__title__istartswith','title__istartswith','user__username__istartswith']
    # prepopulated_fields = {'sentiment':('rating',)}

    # def get_readonly_fields(self, request, obj=None):
    #     ro = ['created_at',]
    #     if obj:
    #         ro += ['sentiment', 'user_name', 'title_media']
    #     return ro

@admin.register(UserMediaStatus)
class AdminUserMediaStatus(BaseAdminInteractions):
    fields = ['title_media','post_photo','user_name','status']
    readonly_fields = ('title_media','user_name','post_photo')
    list_display = ('id', 'title_media','post_photo','user_name','status')
    list_display_links = ('id', 'user_name','title_media')
    list_filter = [MediaTypeFilter,'status']
    ordering = ['id']
    search_fields = ['mediaitem__title__istartswith',  'user__username__istartswith']
    actions = ['delete_status_none',]

    @admin.action(description='Удалить ВСЕ записи со статусом «Без статуса»')
    def delete_status_none(self, request, queryset):
        queryset.filter(
            status=UserMediaStatus.Status.NONE
        ).delete()
