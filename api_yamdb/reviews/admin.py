from django.contrib import admin

from reviews.models import (
    Title,
    Genre,
    Category,
    User,
    Review
)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'rating',
        'display_genres',
        'description'
    )

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    display_genres.short_description = 'Genres'

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


admin.site.register(User)
