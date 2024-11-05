from django.contrib.auth import get_user_model

from django.urls import reverse
from django.test import Client, TestCase

from notes.models import Note
from ..forms import WARNING

User = get_user_model()


class TestFixture(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.commentator = User.objects.create(username='Автор комментария')
        cls.login_author = Client()
        cls.login_reader = Client()
        cls.login_commentator = Client()
        cls.login_author.force_login(cls.author)
        cls.login_reader.force_login(cls.reader)
        cls.login_commentator.force_login(cls.commentator)
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )
        notes = [
            Note(
                title=f'Новость{index}',
                text='Просто текст.',
                author=cls.author,
                slug=f'note-{index}'
            )
            for index in range(9)
        ]
        Note.objects.bulk_create(notes)

        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Текст1',
            'slug': 'slug'
        }
        cls.form_data_not_slug = {
            'title': 'Заголовок',
            'text': 'Текст1',
            'slug': ''
        }
        cls.add = reverse(
            'notes:add'
        )
        cls.detail = reverse(
            'notes:detail', args=(cls.notes.slug,)
        )
        cls.list = reverse(
            'notes:list'
        )
        cls.success = reverse(
            'notes:success'
        )
        cls.home = reverse(
            'notes:home'
        )
        cls.login = reverse(
            'users:login'
        )
        cls.logout = reverse(
            'users:logout'
        )
        cls.signup = reverse(
            'users:signup'
        )
        cls.url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=(cls.notes.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.notes.slug,))
        cls.warning = WARNING
