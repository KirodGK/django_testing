from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

import pytest


@pytest.mark.parametrize(
    "test_url", (
        pytest.lazy_fixture('home'),
        pytest.lazy_fixture('login'),
        pytest.lazy_fixture('logout'),
        pytest.lazy_fixture('signup'),
        pytest.lazy_fixture('detail'),
    )
)
def test_pages_availability_anonymous_user(client, test_url, news):
    """Доступность страниц для пользователя."""
    url = test_url
    response = client.get(url)
    print(client)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (pytest.lazy_fixture('delete'), pytest.lazy_fixture('author_client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('edit'), pytest.lazy_fixture('author_client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('delete'), pytest.lazy_fixture('admin_client'),
         HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('edit'), pytest.lazy_fixture('admin_client'),
         HTTPStatus.NOT_FOUND),
    )
)
def test_redirects(reverse_url, parametrized_client, status):
    """Доступность страниц удаления и редактирования."""
    url = reverse_url
    response = parametrized_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'urls',
    (
        pytest.lazy_fixture('delete'),
        pytest.lazy_fixture('edit'),
    ),
)
def test_redirects(client, urls):
    """Перенаправлние при запросе страниц удаления и редактирования записей\
        другого автора."""
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={urls}'
    response = client.get(urls)
    assertRedirects(response, expected_url)
