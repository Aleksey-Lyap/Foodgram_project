from django.contrib import admin

from recipes.models import (Cart, Favorite, Ingredient, IngredientsRecipe,
                            Recipe, Tag, TagRecipe)


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    min_num = 1


class IngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorites')
    inlines = [
        IngredientsInline,
        TagInline,
    ]
    list_filter = ('author', 'name', 'tags')

    def favorites(self, obj):
        return obj.favorites.count()

    favorites.short_description = 'В избранном'


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(IngredientsRecipe)
admin.site.register(TagRecipe)
admin.site.register(Favorite)
admin.site.register(Cart)
