from django.db import models
from django.urls import reverse


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('pdrn', 'PDRN'),
        ('plla', 'PLLA'),
        ('filler', 'Филлер'),
    ]

    name = models.CharField('Название', max_length=255)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES, blank=True)
    price = models.PositiveIntegerField('Цена')
    old_price = models.PositiveIntegerField('Старая цена', null=True, blank=True)
    discount = models.PositiveIntegerField('Скидка, %', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Фото', upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.pk])