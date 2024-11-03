from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note
from .test_fixture import TestFixture
from ..forms import NoteForm

User = get_user_model()


class TestNotesPage(TestFixture):

    NOTES_URL = reverse('notes:list')

    def test_notes_list(self):
        """Наличие заметок в спике вывода"""
        response = self.login_author.get(self.NOTES_URL)
        object_list_main = response.context['object_list']
        self.notes = Note.objects.create(
            title='Заголовок test_notes_list',
            text='Текст',
            author=self.author
        )
        object_list_last = response.context['object_list']
        self.assertNotIn(object_list_last, object_list_main)

    def test_reader_context_list(self):
        """Наличие заметок другого автора"""
        response = self.login_reader.get(self.NOTES_URL)
        object_list = response.context['object_list']
        notes_author = self.author
        self.assertNotIn(notes_author, object_list)


class TestAddAndEditPage(TestFixture):

    def test_form(self):
        """Доступность форм редактирования и добавления заметок."""
        urls = (self.edit, self.add)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.login_author.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context.get("form"), NoteForm)
