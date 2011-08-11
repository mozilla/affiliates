from django.contrib import admin

from affiliates.admin import site
from badges.models import Category, Subcategory


class CategoryAdmin(admin.ModelAdmin):
    pass
site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    pass
site.register(Subcategory, SubcategoryAdmin)
