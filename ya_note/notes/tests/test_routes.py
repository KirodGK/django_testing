from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from .test_fixture import TestFixture

User = get_user_model()


class TestRoutes(TestFixture):

    def test_pages_availability(self):
        """Проверка доступности страниц для всех пользователей."""
        urls = (
            self.home, self.login, self.logout, self.signup
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def page_available_authorized_user(self):
        """Проверка доступности страниц для залогиненного пользователя."""
        urls = (
            self.list, self.success, self.add,
        )
        for name, args in urls:
            
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.login_author.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_anonymous_client(self):
        """Проверка перенаправление незалогиненного пользователя."""
        login_url = reverse('users:login')
        urls = (
            self.edit, self.delete, ('notes:detail', (self.notes.slug,)),
            self.list, self.success,
            self.add
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_availability_edit_delite_detail(self):
        """Проверка доступности страниц только автору."""
        users_statuses = (
            (self.login_author, HTTPStatus.OK),
            (self.login_reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client = user
            for name, item in (self.edit, self.delete, self.detail):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=item)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)
