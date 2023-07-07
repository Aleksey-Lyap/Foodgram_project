from django.contrib import admin
from recipes.models import Recipe, Tag, Ingredients,  IngredientsRecipe, TagRecipe, Favorite, Cart


admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredients)
admin.site.register(IngredientsRecipe)
admin.site.register(TagRecipe)
admin.site.register(Favorite)
admin.site.register(Cart)


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#  list_display = ['author', 'name', 'image', 'text', 'ingredients', 'tags', 'cooking_time', 'create_date']
#  list_filter = ['status', 'created', 'publish', 'author']
#  search_fields = ['title', 'body']
#  prepopulated_fields = {'slug': ('title',)}
#  raw_id_fields = ['author']
#  date_hierarchy = 'publish'
#  ordering = ['status', 'publish']