
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Article, UserFavouriteArticle


User = get_user_model()


class ProtectedViewsTest(TestCase):
    """Ensure protected views redirect anonymous users to login."""

    def setUp(self):
        self.client = Client()

    def test_favourites_publications_publish_redirect_anonymous(self):
        protected_routes = ['favourites', 'publications', 'publish']

        for route_name in protected_routes:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(f'ex:{route_name}'))
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse('ex:login'), response.url)
                if route_name == 'publish':
                    self.assertIn('next=', response.url)


class RegisterAccessTest(TestCase):
    """Ensure authenticated users cannot access register form."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='registered_user',
            password='secure-pass-123',
        )

    def test_logged_in_user_is_redirected_from_register(self):
        self.client.login(username='registered_user', password='secure-pass-123')

        response = self.client.get(reverse('ex:register'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('ex:home'))


class FavouriteDuplicateTest(TestCase):
    """Ensure the same article cannot be added twice to favourites."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='reader_user',
            password='reader-pass-123',
        )
        self.author = User.objects.create_user(
            username='author_user',
            password='author-pass-123',
        )
        self.article = Article.objects.create(
            title='Testing duplicates',
            author=self.author,
            synopsis='Short synopsis for duplicate favourite test.',
            content='Long content for duplicate favourite test.',
        )

    def test_cannot_add_same_article_twice_via_view(self):
        self.client.login(username='reader_user', password='reader-pass-123')

        url = reverse('ex:add-favourite', kwargs={'pk': self.article.pk})
        payload = {'article': self.article.pk}

        first_response = self.client.post(url, payload)
        second_response = self.client.post(url, payload)

        self.assertEqual(first_response.status_code, 302)
        self.assertEqual(second_response.status_code, 302)
        self.assertEqual(
            UserFavouriteArticle.objects.filter(
                user=self.user,
                article=self.article,
            ).count(),
            1,
        )