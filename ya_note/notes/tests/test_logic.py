from http import HTTPStatus
from pytils.translit import slugify

from django.contrib.auth import get_user_model
from django.test import Client
from .test_fixture import TestFixture
from ..models import Note
from ..forms import NoteForm
User = get_user_model()


class TestnotesCreation(TestFixture):


    def test_anonymous_user_cant_create_notes(self):
        """Проверка создания заметки незалогиненного пользователя."""
        notes_count_main = Note.objects.count()
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_main)

    def test_user_can_create_notes(self):
        """Проверка создания заметки пользователем."""
        notes_count_main = Note.objects.count()
        self.login_author.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_main+1)
        notes = Note.objects.get(id=notes_count)
        self.assertEqual(notes.text, self.form_data.get("text"))
        self.assertEqual(notes.title, self.form_data.get("title"))
        self.assertEqual(notes.author, self.form_data.get("author"))

    def test_two_slug(self):
        """создание дублирующих уникальныйх полей."""
        self.login_author.post(self.url, data=self.form_data)
        notes_count_main = Note.objects.count()
        self.login_author.post(self.url, data=self.form_data)
        notes_count_last = Note.objects.count()
        self.assertEqual(notes_count_last, (notes_count_main))
        response = self.login_author.post(self.url, data=self.form_data)
        notes_count_2 = Note.objects.count()
        self.assertEqual(notes_count_2, notes_count_main)
        self.assertFormError(response, 'form', 'slug',  f'slug{self.warning}')

    def test_auto_creation_slug(self):
        """функция автоматической генерации slug."""
        self.login_author.post(self.url, data=self.form_data)
        notes_count_main = Note.objects.count()
        self.login_author.post(self.url, data=self.form_data)
        notes_count_last = Note.objects.count()
        notes = self.notes
        self.assertEqual(notes_count_main, notes_count_last)
        self.assertEqual(notes.slug, slugify(notes.title))


class TestnotesEditDelete(TestFixture):

    def test_author_can_delete_notess(self):
        """Проверка удаления автором."""
        notes_count_main = Note.objects.count()
        response = self.login_author.delete(self.delete_url)
        self.assertRedirects(response, self.note_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, (notes_count_main-1))

    def test_user_cant_delete_notes_of_another_user(self):
        """Запрет удаления заметки другого пользователя."""
        notes_count_main = Note.objects.count()
        response = self.login_reader.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_main)

    def test_author_can_edit_notes(self):
        """Редактирование заметки автором."""
        response = self.login_author.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.note_url)
        first_id = self.notes.id
        note = Note.objects.get(id=first_id)
        self.login_author.post(self.edit_url, data=self.form_data)
        title, text, author, slug = self.form_data.values()
        self.assertEqual(note.text, text)
        self.assertEqual(note.title, title)
        self.assertEqual(note.author, author)

    def test_user_cant_edit_notes_of_another_user(self):
        """Запрет редактирование  заметки другого автора."""
        response = self.login_reader.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        first_id = self.notes.id
        note = Note.objects.get(id=first_id)
        title, text, author, slug = self.form_data.values()
        self.assertNotEqual(note.text, text)
        self.assertEqual(note.title, title)
        self.assertEqual(note.author, author)
