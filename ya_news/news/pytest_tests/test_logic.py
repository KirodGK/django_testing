from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment 
from .const import FORM_DATA  


def test_user_create_comment(author_client, detail, author, news,
                             comment):
    """Создание комментария авторизованный автором."""
    comments_count = Comment.objects.count()
    url = detail
    response = author_client.post(url, data=FORM_DATA)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == comments_count + 1
    new_comment = Comment.objects.last()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_anonymous_user_create_news(client, detail, news, login):
    """Создание записи неавторизованный пользователем."""
    comments_count = Comment.objects.count()
    response = client.post(detail, data=FORM_DATA)
    expected_url = f'{login}?next={detail}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comments_count


def test_user_used_bad_words(author_client, detail, news):
    """Проверка использования запрещённых слов."""
    comments_count = Comment.objects.count()
    data_bad_words = {}
    data_bad_words['text'] = f'{BAD_WORDS[0]} текст'
    response = author_client.post(detail, data=data_bad_words)
    assert Comment.objects.count() == comments_count
    assertFormError(response, 'form', 'text', errors=(WARNING))


def test_author_delete_comment(author_client, delete, detail_comment, news,
                               comment):
    """Удаления комментария автором."""
    comments_count = Comment.objects.count()
    response = author_client.delete(delete)
    assertRedirects(response, detail_comment)
    assert Comment.objects.count() == comments_count - 1


def test_author_edit_comment(author_client, author, edit, detail_comment,
                             news, comment):
    """Редактирование комментария автором."""
    comments_count = Comment.objects.count()
    response = author_client.post(edit, data=FORM_DATA)
    new_comment = Comment.objects.get(id=comment.id)
    assert Comment.objects.count() == comments_count
    assert new_comment.text != comment.text
    assert new_comment.author == comment.author
    assert new_comment.news == comment.news
    assertRedirects(response, detail_comment)


def test_user_delete_comment_of_another_user(reader_client, comment, delete):
    """Запрет удаление комментария другого пользователя."""
    comments_count = Comment.objects.count()
    response = reader_client.delete(delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count


def test_user_edit_comment_of_another_user(
        reader_client,
        comment,
        edit
):
    """Запрет редактирования комментария другого пользователя."""
    response = reader_client.post(edit, data=FORM_DATA)
    last_comment = Comment.objects.get(id=comment.id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == last_comment.text
    assert comment.author == last_comment.author
    assert comment.news == last_comment.news
