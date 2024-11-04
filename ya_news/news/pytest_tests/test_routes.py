from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from .const import  NOT_FOUND, SUCCESSFULLY_COMPLETED


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (lf('delete'), lf('author_client'), SUCCESSFULLY_COMPLETED),
        (lf('edit'), lf('author_client'), SUCCESSFULLY_COMPLETED),
        (lf('delete'), lf('admin_client'), NOT_FOUND),
        (lf('edit'), lf('admin_client'), NOT_FOUND),
        (lf('home'), lf('admin_client'), SUCCESSFULLY_COMPLETED),
        (lf('login'), lf('admin_client'), SUCCESSFULLY_COMPLETED),
        (lf('logout'), lf('admin_client'), SUCCESSFULLY_COMPLETED),
        (lf('signup'), lf('admin_client'), SUCCESSFULLY_COMPLETED),
        (lf('detail'), lf('admin_client'), SUCCESSFULLY_COMPLETED),
    )
)
def test_redirects_all(reverse_url, parametrized_client, status):
    """Доступность страниц удаления и редактирования."""
    url = reverse_url
    response = parametrized_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'urls',
    (
        lf('delete'),
        lf('edit'),
    ),
)
def test_redirects(client, urls, login):
    """Перенаправлние при запросе страниц удаления и редактирования записей\
        другого автора."""
    expected_url = f'{login}?next={urls}'
    response = client.get(urls)
    assertRedirects(response, expected_url)
