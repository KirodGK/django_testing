from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_user_create_comment(author_client, author, form_data, news):
    """Создание комментария авторизованный автором."""
    comments_count = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == comments_count + 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_anonymous_user_create_news(client, form_data, news):
    """Создание записи неавторизованный пользователем."""
    comments_count = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comments_count


def test_user_used_bad_words(author_client, news, form_data):
    """Проверка использования запрещённых слов."""
    comments_count = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    form_data['text'] = f'{BAD_WORDS[0]} текст'
    response = author_client.post(url, data=form_data)
    assertFormError(response, 'form', 'text', errors=(WARNING))
    assert Comment.objects.count() == comments_count


def test_author_delete_comment(author_client, news, comment):
    """Удаления комментария автором."""
    comments_count = Comment.objects.count()
    url_to_comments = reverse('news:detail', args=(news.id,)) + '#comments'
    url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == comments_count - 1


def test_author_edit_comment(author_client, news, form_data, comment):
    """Редактирование комментария автором."""
    comments_count = Comment.objects.count()
    url_to_comments = reverse('news:detail', args=(news.id,)) + '#comments'
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == comments_count


def test_user_delete_comment_of_another_user(reader_client, comment):
    """Запрет удаление комментария другого пользоватлея."""
    comments_count = Comment.objects.count()
    url = reverse('news:delete', args=(comment.id,))
    response = reader_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count


def test_user_edit_comment_of_another_user(
        reader_client,
        form_data,
        comment
):
    """Запрет редактирования комментария другого пользователя."""
    url = reverse('news:edit', args=(comment.id,))
    response = reader_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
