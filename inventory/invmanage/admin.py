from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
    ProductAllocation,
)

admin.site.register(Category, MPTTModelAdmin)

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue

class AllocationInline(admin.TabularInline):
    model = ProductAllocation

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
        AllocationInline,
    ]

    list_display = ["name", "category", "total_count", "remaining_count"]
    search_fields = ["name", "category__name"]
    list_filter = ["category", "is_active"]

@admin.register(ProductAllocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity_allocated", "allocated_to"]
    search_fields = ["product__title", "allocated_to"]
    list_filter = ["product"]
