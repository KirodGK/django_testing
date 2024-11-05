from django.conf import settings

from news.forms import CommentForm
from .const import FORM_DATA


def test_home_page(client, home, news_list_generate):
    """Проверка работы пагинации."""
    response = client.get(home)
    assert response.context['object_list'].count() == (settings.
                                                       NEWS_COUNT_ON_HOME_PAGE)


def test_news_order(client, home, news_list_generate):
    """Проверка работы сортировки записей."""
    response = client.get(home)
    all_dates = [news.date for news in response.context['object_list']]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, detail, commets):
    """Проверка работы сортировки комментариев."""
    response = client.get(detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_date_created = [comment.created for comment in all_comments]
    sorted_date = sorted(all_date_created)
    assert all_date_created == sorted_date


def test_detail_page_contains_form(author_client, detail, news):
    """Проверка наличия формы комментариев для авторизованного автора."""
    response = author_client.get(detail, data=FORM_DATA)
    form = response.context['form']
    assert 'form' in response.context
    assert isinstance(form, CommentForm)


def test_detail_page_contains_form_user(client, detail, news):
    """Проверка наличия формы  для авторизованного пользователя."""
    response = client.get(detail)
    assert 'form' not in response.context
