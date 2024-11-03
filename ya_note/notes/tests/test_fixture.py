from django.contrib.auth import get_user_model
from django.urls import reverse

from django.test import Client, TestCase

from notes.models import Note

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
            'author': cls.author,
            'slug': 'slug'
        }
        cls.form_data_not = {
            'title': 'Заголовок',
            'text': 'Текст1',
            'author': cls.author,
            'slug': 'slug'
        }
        cls.edit = (
            'notes:edit', (cls.notes.slug,)
        )
        cls.add = (
            'notes:add', None
        )
        cls.delete = (
            'notes:delete', (cls.notes.slug,)
        )
        cls.detail = (
            'notes:detail', (cls.notes.slug,)
        )
        cls.list = (
            'notes:list', None
        )
        cls.success = (
            'notes:success', None
        )
        cls.home = (
            'notes:home', None
        )
        cls.login = (
            'users:login', None
        )
        cls.logout = (
            'users:logout', None
        )
        cls.signup = (
            'users:signup', None
        )
        
        cls.url = reverse('notes:add', args=None)
        cls.note_url = reverse('notes:success', args=None)
        cls.edit_url = reverse('notes:edit', args=(cls.notes.slug,))
        cls.delete_url = reverse('notes:delete',  args=(cls.notes.slug,))
        cls.warning = ' - такой slug уже существует, придумайте уникальное значение!'
        
    
        #  urls = (
        #     ('notes:home', None),
        #     ('users:login', None),
        #     ('users:logout', None),
        #     ('users:signup', None),
        # )
