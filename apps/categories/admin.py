from django.contrib import admin
from .models import Category, SubCategory, SubSubCategory

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    prepopulated_fields = {'slug': ('name',)}

class SubSubCategoryInline(admin.TabularInline):
    model = SubSubCategory
    extra = 1
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubSubCategoryInline]

@admin.register(SubSubCategory)
class SubSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'slug', 'order', 'is_active')
    list_filter = ('subcategory__category', 'subcategory', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
