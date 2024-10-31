from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from notes.models import Note
from .test_fixture import TestFixture

User = get_user_model()


class TestNotesPage(TestFixture):

    NOTES_URL = reverse('notes:list')

    def test_notes_list(self):
        """Наличие заметок в спике вывода"""
        
        response = self.login_author.get(self.NOTES_URL)
        object_list = response.context['object_list']
        first_note = self.notes
        self.assertIn(first_note, object_list)

    def test_reader_context_list(self):
        """Наличие заметок другого автора"""
        
        response = self.login_reader.get(self.NOTES_URL)
        object_list = response.context['object_list']
        notes_count = len(object_list)
        self.assertEqual(notes_count, 0)

    def test_author_context_list(self):
        """Наличие заметок автора"""
        response = self.login_author.get(self.NOTES_URL)
        object_list = response.context['object_list']
        notes_count = len(object_list)
        self.assertEqual(notes_count, 10)


class TestAddAndEditPage(TestFixture):

    def test_form(self):
        """Доступность форм редактирования и добавления заметок."""
        
        urls = (
            ('notes:edit', (self.notes.slug,)),
            ('notes:add', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.login_author.get(url)
                self.assertIn('form', response.context)
