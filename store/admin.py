from django.contrib import admin
from django.utils.html import format_html
from .models import Product

admin.site.site_header = 'Dr. Isana — админка'
admin.site.site_title = 'Dr. Isana'
admin.site.index_title = 'Управление магазином'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'category', 'price', 'old_price', 'created_at')
    list_display_links = ('thumbnail', 'name')
    list_editable = ('price',)
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'image_preview')

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'category', 'description'),
        }),
        ('Цена', {
            'fields': ('price', 'old_price', 'discount'),
            'description': 'Старая цена и скидка — необязательные, заполняйте только если товар со скидкой.',
        }),
        ('Фото', {
            'fields': ('image', 'image_preview'),
        }),
        ('Служебное', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:8px;">',
                obj.image.url,
            )
        return format_html('<span style="color:#999;">нет фото</span>')
    thumbnail.short_description = ''

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:280px;border-radius:12px;border:1px solid #E6ECF5;">',
                obj.image.url,
            )
        return 'Фото ещё не загружено'
    image_preview.short_description = 'Предпросмотр'