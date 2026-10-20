from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Product, Review


class ReviewsPageTests(TestCase):
    def test_shows_reviews_added_in_admin(self):
        Review.objects.create(name='Айгерим, косметолог', quote='Всё пришло в тот же день')

        response = self.client.get(reverse('store:reviews'))

        self.assertContains(response, 'Всё пришло в тот же день')
        self.assertContains(response, 'Айгерим, косметолог')

    def test_no_placeholder_text_when_there_are_no_reviews(self):
        response = self.client.get(reverse('store:reviews'))

        self.assertNotContains(response, 'Добавьте текст отзыва')
        self.assertContains(response, 'Отзывы скоро появятся здесь.')


class ProductWithoutImageTests(TestCase):
    def test_pages_open_when_product_has_no_image(self):
        product = Product.objects.create(name='Товар без фото', price=1000, category='pdrn')

        for url in [reverse('store:home'), reverse('store:catalog'), product.get_absolute_url()]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)


class AdminNavigationTests(TestCase):
    def test_admin_link_is_hidden_for_anonymous_users(self):
        response = self.client.get(reverse('store:home'))

        self.assertNotContains(response, 'Личный кабинет')

    def test_admin_link_is_hidden_for_regular_users(self):
        user = get_user_model().objects.create_user(username='customer', password='password')
        self.client.force_login(user)

        response = self.client.get(reverse('store:home'))

        self.assertNotContains(response, 'Личный кабинет')

    def test_admin_link_is_visible_for_active_staff_users(self):
        user = get_user_model().objects.create_user(
            username='admin',
            password='password',
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('store:home'))

        self.assertContains(response, 'Личный кабинет')

    def test_admin_link_is_hidden_for_inactive_staff_users(self):
        user = get_user_model().objects.create_user(
            username='inactive-admin',
            password='password',
            is_staff=True,
            is_active=False,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('store:home'))

        self.assertNotContains(response, 'Личный кабинет')

    def test_regular_users_cannot_access_admin(self):
        user = get_user_model().objects.create_user(username='customer', password='password')
        self.client.force_login(user)

        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, 302)
