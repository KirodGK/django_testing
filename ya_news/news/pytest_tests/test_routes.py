import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.models import News


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', pytest.lazy_fixture('id_news_for_args')),
    ),
)
def test_pages_availability_anonymous_user(client, name, args, news):
    """Доступность страниц для пользователя."""
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
def test_pages_availability_author(author_client, name, comment):
    """Доступность страниц удаления и редактирования  для автора."""
    url = reverse(name, args=(comment.id,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
def test_pages_availability_different_users(
        parametrized_client, name, comment, expected_status
):
    """Доступность страниц удаления и редактирования для пользователей."""
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('id_comment_for_args')),
        ('news:edit', pytest.lazy_fixture('id_comment_for_args')),
    ),
)
def test_redirects(client, name, args):
    """Перенаправлние при запросе страниц удаления и редактирования записей\
        другого автора."""
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
