from http import HTTPStatus

from django.contrib.auth import get_user_model

from .test_fixture import TestFixture

User = get_user_model()


class TestRoutes(TestFixture):

    def test_pages_availability(self):
        """Проверка доступности страниц для всех пользователей."""
        urls = (
            self.home, self.login, self.logout, self.signup
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def page_available_authorized_user(self):
        """Проверка доступности страниц для залогиненного пользователя."""
        urls = (
            self.list, self.success, self.add,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.login_author.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_anonymous_client(self):
        """Проверка перенаправление незалогиненного пользователя."""
<<<<<<< HEAD
        urls = (
            self.edit_url, self.delete_url, self.detail,
            self.list, self.success,
            self.add
        )
        for url in urls:
            with self.subTest(url=url):
=======
        urls = (self.edit, self.delete, self.detail, self.list, self.success,
                self.add)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
>>>>>>> 1ec109f3bbda96288489efa7e8c009d05d269302
                redirect_url = f'{self.login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_availability_edit_delite_detail(self):
        """Проверка доступности страниц только автору."""
        users_statuses = (
            (self.login_author, HTTPStatus.OK),
            (self.login_reader, HTTPStatus.NOT_FOUND),
        )
        urls = (self.edit_url, self.delete_url, self.detail)
        for user, status in users_statuses:
            self.client = user
<<<<<<< HEAD
            for url in urls:
                with self.subTest(user=user, url=url):
=======
            for name, item in (self.edit, self.delete, self.detail):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=item)
>>>>>>> 1ec109f3bbda96288489efa7e8c009d05d269302
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)
