from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(
        max_length=144,
    )
    slug = models.SlugField(
        verbose_name='Человекочитаемый URL.',
        unique=True,
        max_length=144
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=144
    )
    slug = models.SlugField(
        verbose_name='Человекочитаемый URL.',
        unique=True,
        max_length=144,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Title(models.Model):
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
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения.',
        null=True,
        default=None
    )


# class GenOfTitle(models.Model):
#     title = models.ForeignKey(
#         Title,
#         on_delete=models.CASCADE
#     )
#     genre = models.ForeignKey(
#         Genre,
#         on_delete=models.SET_NULL
#     )

#     def __str__(self) -> str:
#         return f'{self.title} - {self.genre}'
