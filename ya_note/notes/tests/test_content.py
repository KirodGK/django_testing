from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note
from .test_fixture import TestFixture
from ..forms import NoteForm

User = get_user_model()


class TestNotesPage(TestFixture):

    def test_notes_list(self):
        """Наличие заметок в спике вывода."""
        response = self.login_author.get(self.list)
        object_list_main = response.context['object_list']
        note_author = Note.objects.filter(author=self.author).first()
        self.assertIn(note_author, object_list_main)

    def test_reader_context_list(self):
        """Наличие заметок другого автора."""
        response = self.login_reader.get(self.list)
        object_list_main = response.context['object_list']
        note_author = Note.objects.filter(author=self.author).first()
        self.assertNotIn(note_author, object_list_main)


class TestAddAndEditPage(TestFixture):

    def test_form(self):
        """Доступность форм редактирования и добавления заметок."""
        urls = (self.url,  self.edit_url)
        for url in urls:
            with self.subTest(url=url):
                response = self.login_author.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context.get("form"), NoteForm)
