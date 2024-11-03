from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError

from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING

from .const import FORM_DATA

def test_user_create_comment(author_client, detail, author, news,
                             comment):
    """Создание комментария авторизованный автором."""
    comments_count = Comment.objects.count()
    url = detail
    response = author_client.post(url, data=FORM_DATA)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == comments_count+1
    comments_count_last = Comment.objects.count()
    new_comment = Comment.objects.get(id=comments_count_last)
    print(new_comment.created)
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_anonymous_user_create_news(client, news):
    """Создание записи неавторизованный пользователем."""
    comments_count = Comment.objects.count()
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=FORM_DATA)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comments_count


def test_user_used_bad_words(author_client, news):
    """Проверка использования запрещённых слов."""
    comments_count = Comment.objects.count()
    data_bad_words = {}
    url = reverse('news:detail', args=(news.id,))
    data_bad_words['text'] = f'{BAD_WORDS[0]} текст'
    response = author_client.post(url, data=data_bad_words)
    assert Comment.objects.count() == comments_count
    assertFormError(response, 'form', 'text', errors=(WARNING))
    


def test_author_delete_comment(author_client, news, comment):
    """Удаления комментария автором."""
    comments_count = Comment.objects.count()
    url_to_comments = reverse('news:detail', args=(news.id,)) + '#comments'
    url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == comments_count - 1


def test_author_edit_comment(author_client, author, news, comment):
    """Редактирование комментария автором."""
    comments_count = Comment.objects.count()
    url_to_comments = reverse('news:detail', args=(news.id,)) + '#comments'
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, data=FORM_DATA)
    new_comment = Comment.objects.get(id=comment.id)
    assert Comment.objects.count() == comments_count
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == author
    assert new_comment.news == news
    assertRedirects(response, url_to_comments)


def test_user_delete_comment_of_another_user(reader_client, comment):
    """Запрет удаление комментария другого пользоватлея."""
    comments_count = Comment.objects.count()
    url = reverse('news:delete', args=(comment.id,))
    response = reader_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count


def test_user_edit_comment_of_another_user(
        reader_client,
        comment
):
    """Запрет редактирования комментария другого пользователя."""
    url = reverse('news:edit', args=(comment.id,))
    new_comment = Comment.objects.get(id=comment.id)
    response = reader_client.post(url, data=FORM_DATA)
    last_comment = Comment.objects.get(id=comment.id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert new_comment.text == last_comment.text
    assert new_comment.author == last_comment.author
    assert new_comment.news == last_comment.news
