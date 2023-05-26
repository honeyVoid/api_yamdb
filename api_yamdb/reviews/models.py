from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLES = [
    (ADMIN, 'Administrator'),
    (MODERATOR, 'Moderator'),
    (USER, 'User'),
]


class User(AbstractUser):
    email = models.EmailField('email address', blank=False, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        default=USER,
        max_length=50,
        blank=True,
        choices=ROLES
    )

    @property
    def is_admin(self):
        if self.role == ADMIN:
            return True

    @property
    def is_moderator(self):
        if self.role == MODERATOR:
            return True

    class Meta:
        ordering = ['username']


class Genre(models.Model):
    """Модель жанра произведения."""
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Человекочитаемый URL.',
        unique=True,
        max_length=50
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории произведения."""
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Человекочитаемый URL.',
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        max_length=144,
        verbose_name='Название произведение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        verbose_name='Категория произведения.',
        default='Категория не выбрана.',
        on_delete=models.SET_NULL,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения.',
        through='GenreTitle'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения.',
        null=True,
        default=None
    )
    year = models.IntegerField(
        verbose_name='Дата релиза.'
    )
    description = models.CharField(
        max_length=254,
        blank=True,
        null=True
    )


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заголовок',
        db_index=True,
        null=False
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        db_index=True,
        null=False
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        null=False,
        validators=(
            MinValueValidator(1, 'Минимальная оценка 1',),
            MaxValueValidator(10, 'Максимальная оценка 10',)
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='title-author'
            ),
        )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    reviw = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        db_index=True,
        null=False
    )
    text = models.TextField(null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        db_index=True,
        null=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
