from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()

class TestFixture(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')

        cls.login_author = Client()
        cls.login_reader = Client()
        cls.login_author.force_login(cls.author)
        cls.login_reader.force_login(cls.reader)
        

        
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )
        all_notes = [
            Note(
                title=f'Новость{index}',
                text='Просто текст.',
                author=cls.author,
                slug=f'note-{index}'
            )
            for index in range(9)
        ]
        Note.objects.bulk_create(all_notes)
    
