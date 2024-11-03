from datetime import timedelta

from django.conf import settings
from django.urls import reverse, reverse_lazy
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
    """Фикстура Автора"""
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
def news_10(author):
    """Фикстура создание записей больше чем паддинг."""
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(title=f'Новость {index}', text='Просто текст.')
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
    all_comments = []
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}'
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()
        all_comments.append(comment)
    return all_comments


@pytest.fixture
def id_news_for_args(news):
    """Фикстура номера записи."""
    return news.id

@pytest.fixture
def id_comment_for_args(comment):
    """Фикстура номера комментария."""
    return comment.id


@pytest.fixture
def form_data():
    """Фикстура текста."""
    return {
        'text': 'Новый техт'
    }

@pytest.fixture
def home():
    return reverse('news:home', None)
@pytest.fixture
def login():
    return reverse('users:login', None)
    
@pytest.fixture
def logout():
    return reverse('users:logout', None)

@pytest.fixture
def signup():
    return reverse('users:signup', None)

@pytest.fixture
def detail(id_news_for_args):
    return reverse('news:detail',  args=[id_news_for_args])

@pytest.fixture
def delete(id_comment_for_args):
    return reverse('news:delete',  args=[id_comment_for_args])
@pytest.fixture
def edit(id_comment_for_args):
    return reverse('news:edit',  args=[id_comment_for_args])
