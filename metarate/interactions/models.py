from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from catalog.models import MediaItem


# Create your models here.

class UserMediaStatus(models.Model):
    class Status(models.TextChoices):
        NONE = 'none', 'Без статуса'
        PLANNED = 'planned', 'Запланировано'
        COMPLETED = 'completed', 'Завершено'

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='media_status',
        verbose_name='Пользователь'
    )
    mediaitem = models.ForeignKey(
        MediaItem,
        on_delete=models.CASCADE,
        related_name='usermediastatus',
        verbose_name='Контент'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NONE,
        verbose_name='Статус',
    )

    def is_planned(self):
        return self.status == self.Status.PLANNED

    def is_completed(self):
        return self.status == self.Status.COMPLETED


    def __str__(self):
        return f"Статус: {self.user} → {self.mediaitem.title} — {self.get_status_display()}"


    class Meta:
        verbose_name = "Статус контента пользователя"
        verbose_name_plural = "Статусы контента пользователей"



class Review(models.Model):
    POSITIVE = 'positive'
    NEUTRAL = 'neutral'
    NEGATIVE = 'negative'

    SENTIMENT_CHOICES = [
        (POSITIVE, 'Положительная'),
        (NEUTRAL, 'Нейтральная'),
        (NEGATIVE, 'Отрицательная'),
    ]

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name = 'Оценка'
    )
    sentiment = models.CharField(max_length=20, blank=True,choices=SENTIMENT_CHOICES,verbose_name='Настроение рецензии')

    title = models.CharField(max_length=60,verbose_name='Название статьи')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',null=True)

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    mediaitem = models.ForeignKey(
        MediaItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews'
    )

    def calculate_type(self):
        if self.rating <= 3:
            return self.NEGATIVE
        if self.rating <= 6:
            return self.NEUTRAL
        return self.POSITIVE

    def save(self, *args, **kwargs):
        if not self.sentiment:
            self.sentiment = self.calculate_type()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"

    def __str__(self):
        return f"{self.user} → {self.mediaitem.title} ({self.rating}/10)"