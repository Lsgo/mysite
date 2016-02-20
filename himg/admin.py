from django.contrib import admin

from .models import Column, Article, User


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'intro', 'nav_display', 'home_display')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'pub_date', 'update_time')
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password')

admin.site.register(Column, ColumnAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(User, UserAdmin)
