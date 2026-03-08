import os

from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from slugify import slugify
from django.urls import reverse


# Create your models here.
class Genre(models.Model):
    CONTENT_TYPE = {
        'movie': 'Фильм',
        'game': 'Игра',
        'book': 'Книга',
     }

    name = models.CharField(max_length=40,unique=True)
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE,
        null=True,
        blank=True)
    slug = models.SlugField(unique=True, default='movie', verbose_name='Slug')

    def __str__(self):
        return f'Жанр: {self.name}'

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args,**kwargs)


class Creator(models.Model):
    TYPE_CREATE = {'director':'Директор',
                   'author':'Автор',
                   'studio':'Студия',
    }
    name = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=40,choices=TYPE_CREATE,default='director')

    def __str__(self):
        return f"{self.TYPE_CREATE[self.type]}: {self.name}"

    def get_type_display(self):
        return self.TYPE_CREATE[self.type]

    class Meta:
        verbose_name = "Создатель"
        verbose_name_plural = "Создатели"

def user_directory_path(instance, filename):
    type = class_name = instance.__class__.__name__.lower()
    ext = os.path.splitext(filename)[1]
    return f'catalog/{type}/{instance.slug}{ext}'

class MediaItem(models.Model):
    URL_PATTERNS = {
        'movie': 'movie_detail',
        'series': 'series_detail',
        'book': 'book_detail',
        'computergame': 'game_detail',
    }

    title = models.CharField(max_length=40,verbose_name='Заголовок')
    year = models.PositiveIntegerField(validators=[MinValueValidator(1895),MaxValueValidator(2025)],null=True,verbose_name='Год')
    description = models.TextField(null=True,blank=True,verbose_name='Краткое описание')
    full_description = models.TextField(null=True, blank=True,verbose_name='Полное описание')
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
        verbose_name = 'Рейтинг'
    )
    poster = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        blank=True,
        default='default_content.png',
        verbose_name = 'Постер'
    )
    genres = models.ManyToManyField(Genre,blank=True,verbose_name='Жанры')
    created_at = models.DateField(auto_now_add=True,verbose_name='Дата создания')
    creator = models.ForeignKey(Creator,on_delete=models.CASCADE,null=True,verbose_name='Создатель')
    country = models.CharField(max_length=40, null=True, blank=True,verbose_name='Страна')
    slug = models.SlugField(null=True,unique=True, blank=True, verbose_name='Slug')
    content_type = models.CharField(max_length=40,null=True,blank=True,verbose_name='Тип контента')
    page_author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Автор записи')

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.content_type = self.__class__.__name__.lower()
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        url = self.URL_PATTERNS[self.content_type]
        return reverse(url,args=[self.slug])

class Movie(MediaItem):
    budget = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'Фильм: {self.title} ({self.year})' if self.year else f'Фильм: {self.title}'

    class Meta:
        verbose_name ='Фильм'
        verbose_name_plural = 'Фильмы'

class Book(MediaItem):
    def __str__(self):
        return f'Книга: {self.title} ({self.year})' if self.year else f'Книга: {self.title}'

    class Meta:
        verbose_name ='Книга'
        verbose_name_plural = 'Книги'



class Series(MediaItem):

    def __str__(self):
        return f'Сериал: {self.title} ({self.year})' if self.year else f'Сериал: {self.title}'

    class Meta:
        verbose_name ='Сериал'
        verbose_name_plural = 'Сериалы'



class ComputerGame(MediaItem):

    budget = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'Игра: {self.title} ({self.year})' if self.year else f'Игра: {self.title}'

    class Meta:
        verbose_name ='Компьютерная игра'
        verbose_name_plural = 'Компьютерные игры'
