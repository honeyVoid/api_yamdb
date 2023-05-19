from django.contrib import admin

from reviews. models import (
    Title,
    Genre,
    Category
)

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'rating',

    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class AdminGenre(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',

    )
    list_filter = ('name',)
    search_fields = ('name', )
