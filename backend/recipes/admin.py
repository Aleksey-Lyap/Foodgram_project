from django.contrib import admin
from recipes.models import Recipe, Tag, Ingredients,  IngredientsRecipe, TagRecipe, Favorite, Cart


admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredients)
admin.site.register(IngredientsRecipe)
admin.site.register(TagRecipe)
admin.site.register(Favorite)
admin.site.register(Cart)