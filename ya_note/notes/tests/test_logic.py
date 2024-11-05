from http import HTTPStatus

from pytils.translit import slugify

from ..models import Note
from .test_fixture import TestFixture


class TestnotesCreation(TestFixture):

    def test_anonymous_user_cant_create_notes(self):
        """Проверка создания заметки незалогиненного пользователя."""
        notes_count_main = Note.objects.count()
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_main)

    def test_user_can_create_notes(self):
        """Проверка создания заметки пользователем."""
        note = Note.objects.all()
        note.delete()
        notes_count_main = Note.objects.count()
        self.login_author.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_main + 1)
        notes = Note.objects.get()
        self.assertEqual(notes.text, self.form_data.get("text"))
        self.assertEqual(notes.title, self.form_data.get("title"))
        self.assertEqual(notes.author, self.author)

    def test_two_slug(self):
        """Cоздание дублирующих уникальныйх полей."""
        notes_count_main = Note.objects.count()
        response = self.login_author.post(self.url,
                                          data=self.form_data_not_slug)
        notes_count_2 = Note.objects.count()
        self.assertEqual(notes_count_2, notes_count_main)
        self.assertFormError(response, 'form', 'slug',
                             f'{self.notes.slug}{self.warning}')

    def test_auto_creation_slug(self):
        """функция автоматической генерации slug."""
        note = Note.objects.all()
        note.delete()
        notes_count_main = Note.objects.all().count()
        self.login_author.post(self.url, data=self.form_data)
        notes_count_last = Note.objects.count()
        notes = Note.objects.get()
        self.assertEqual(notes_count_main + 1, notes_count_last)
        self.assertEqual(notes.slug, slugify(notes.slug))


class TestnotesEditDelete(TestFixture):

    def test_author_can_delete_notess(self):
        """Проверка удаления автором."""
        notes_count_main = Note.objects.count()
        response = self.login_author.delete(self.delete_url)
        self.assertRedirects(response, self.success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, (notes_count_main - 1))

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
        self.assertRedirects(response, self.success)
        first_slug = self.form_data["slug"]
        note = Note.objects.get(slug=first_slug)
        title, text, slug = self.form_data.values()
        self.assertEqual(note.text, text)
        self.assertEqual(note.title, title)
        self.assertEqual(note.author, self.author)

    def test_user_cant_edit_notes_of_another_user(self):
        """Запрет редактирование  заметки другого автора."""
        note_main = self.notes
        response = self.login_reader.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_last = Note.objects.get(id=note_main.id)
        self.assertEqual(note_main.text, note_last.text)
        self.assertEqual(note_main.title, note_last.title)
        self.assertEqual(note_main.slug, note_last.slug)
        self.assertEqual(note_main.author, self.author)
