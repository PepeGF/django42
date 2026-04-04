from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Article, UserFavouriteArticle

User = get_user_model()


class AccessControlAndFavouritesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        self.other = User.objects.create_user(username="o", password="p")
        self.article = Article.objects.create(
            title="T", author=self.other, synopsis="synopsis", content="content"
        )

    def test_favourites_view_requires_authentication_and_uses_template(self):
        url = reverse('ex:favourites')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username="u", password="p")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "ex/favourite.html")

    def test_publications_view_requires_authentication_and_uses_template(self):
        url = reverse('ex:publications')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username="u", password="p")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "ex/publications.html")

    def test_publish_view_requires_authentication_and_uses_template(self):
        url = reverse('ex:publish')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username="u", password="p")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "ex/publish.html")

    def test_authenticated_user_cannot_access_registration_form(self):
        url = reverse('ex:register')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username="u", password="p")
        resp = self.client.get(url)
        self.assertNotEqual(resp.status_code, 200)

    def test_user_cannot_add_same_article_twice_to_favourites(self):
        add_url = reverse('ex:add-favourite', kwargs={'pk': self.article.pk})
        self.client.login(username="u", password="p")
        resp1 = self.client.post(add_url, follow=True)
        self.assertEqual(
            UserFavouriteArticle.objects.filter(user=self.user, article=self.article).count(), 1
        )
        resp2 = self.client.post(add_url, follow=True)
        self.assertEqual(
            UserFavouriteArticle.objects.filter(user=self.user, article=self.article).count(), 1
        )
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Article, UserFavouriteArticle

User = get_user_model()


class FavouritesAndAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        self.other = User.objects.create_user(username="o", password="p")
        self.article = Article.objects.create(
            title="T", author=self.other, synopsis="synopsis", content="content"
        )

    def test_favourites_view_requires_login_and_uses_template_for_authenticated(self):
        url = reverse('ex:favourites')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username="u", password="p")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "ex/favourite.html")

    def test_publications_view_requires_login_and_uses_template_for_authenticated(self):
        url = reverse('ex:publications')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username="u", password="p")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "ex/publications.html")

    def test_publish_view_requires_login_and_uses_template_for_authenticated(self):
        url = reverse('ex:publish')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.login(username="u", password="p")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "ex/publish.html")

    def test_authenticated_user_cannot_access_registration_form(self):
        url = reverse('ex:register')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username="u", password="p")
        resp = self.client.get(url)
        self.assertNotEqual(resp.status_code, 200)

    def test_user_cannot_add_same_article_twice_to_favourites(self):
        add_url = reverse('ex:add-favourite', kwargs={'pk': self.article.pk})
        self.client.login(username="u", password="p")
        resp1 = self.client.post(add_url, follow=True)
        self.assertEqual(UserFavouriteArticle.objects.filter(user=self.user, article=self.article).count(), 1)
        resp2 = self.client.post(add_url, follow=True)
        self.assertEqual(UserFavouriteArticle.objects.filter(user=self.user, article=self.article).count(), 1)
from django.test import TestCase

# Create your tests here.
