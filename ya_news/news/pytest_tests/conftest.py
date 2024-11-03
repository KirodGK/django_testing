from datetime import datetime, timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.test import Client

import pytest

from news.models import News, Comment


@pytest.fixture
def reader(django_user_model):
    """Фикстура Читателя."""
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader):
    """Фикстура авторизованного Читателя."""
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def author(django_user_model):
    """Фикстура Автора."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    """Фикстура авторизованного Автора."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def news(author):
    """Фикстура создания Новости."""
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def news_list_generate(author):
    """Фикстура создание записей больше чем паддинг."""
    all_news = []
    today = datetime.today()

    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(title=f'Новость {index}', text='Просто текст.',
                    date=today - timedelta(days=index))
        all_news.append(news)
    return News.objects.bulk_create(all_news)


@pytest.fixture
def comment(author, news):
    """Фикстура создания комментария."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def commets(author, news):
    """Фикстура создания нескольких комментариев."""
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}'
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def home():
    """Фикстура url home."""
    return reverse('news:home', None)


@pytest.fixture
def login():
    """Фикстура url login."""
    return reverse('users:login', None)


@pytest.fixture
def logout():
    """Фикстура url logout."""
    return reverse('users:logout', None)


@pytest.fixture
def signup():
    """Фикстура url signup."""
    return reverse('users:signup', None)


@pytest.fixture
def detail(news):
    """Фикстура url detail."""
    return reverse('news:detail', args=[news.id])


@pytest.fixture
def delete(comment):
    """Фикстура url delete."""
    return reverse('news:delete', args=[comment.id])


@pytest.fixture
def edit(comment):
    """Фикстура url edit."""
    return reverse('news:edit', args=[comment.id])
