from django.contrib import admin
from .models import Article, UserFavouriteArticle



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created")
    search_fields = ("title", "synopsis")
    list_filter = ("created", "author")

@admin.register(UserFavouriteArticle)
class UserFavouriteArticleAdmin(admin.ModelAdmin):
    list_display = ("user", "article")
    search_fields = ("user__username", "article__title")




# Estos serían la versión básica de las clases admin,
# se podrían dejar así por defecto

# admin.site.register(Article)
# admin.site.register(UserFavouriteArticle)