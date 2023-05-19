from django.db import models
# from django.utils.text import slugify


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
