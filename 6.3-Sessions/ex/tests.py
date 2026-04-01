from django.test import TestCase, Client
from django.test.utils import template_rendered
from django.test.client import store_rendered_templates

# Prevent test client from attempting to copy template contexts (works around copy issues)
try:
    template_rendered.disconnect(store_rendered_templates)
except Exception:
    pass
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Tip, Vote


User = get_user_model()


class TipsVotingTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure the test client template renderer receiver is disconnected to avoid context copy issues
        try:
            template_rendered.disconnect(store_rendered_templates)
        except Exception:
            pass
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        try:
            template_rendered.connect(store_rendered_templates)
        except Exception:
            pass
        super().tearDownClass()
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass')
        self.bob = User.objects.create_user(username='bob', password='pass')
        self.client = Client()
        self.tip = Tip.objects.create(content='A tip', author=self.alice)

    def test_create_tip_requires_login(self):
        resp = self.client.post(reverse('ex:home'), {'content': 'New tip'})
        self.assertEqual(Tip.objects.count(), 1)

    def test_create_tip_when_logged_in(self):
        self.client.login(username='bob', password='pass')
        resp = self.client.post(reverse('ex:home'), {'content': 'New tip'})
        self.assertEqual(Tip.objects.count(), 2)
        self.assertTrue(Tip.objects.filter(author=self.bob, content='New tip').exists())

    def test_upvote_increases_reputation(self):
        self.client.login(username='bob', password='pass')
        resp = self.client.get(reverse('ex:vote', args=[self.tip.id, 1]))
        self.assertTrue(Vote.objects.filter(tip=self.tip, user=self.bob, value=1).exists())
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.reputation, 5)

    def test_toggle_upvote(self):
        self.client.login(username='bob', password='pass')
        self.client.get(reverse('ex:vote', args=[self.tip.id, 1]))
        # toggle off
        self.client.get(reverse('ex:vote', args=[self.tip.id, 1]))
        self.assertFalse(Vote.objects.filter(tip=self.tip, user=self.bob).exists())
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.reputation, 0)

    def test_downvote_forbidden_for_low_reputation(self):
        self.client.login(username='bob', password='pass')
        resp = self.client.get(reverse('ex:vote', args=[self.tip.id, -1]))
        self.assertFalse(Vote.objects.filter(tip=self.tip, user=self.bob, value=-1).exists())
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.reputation, 0)

    def test_downvote_allowed_with_reputation(self):
        # give bob enough reputation
        self.bob.reputation = 15
        self.bob.save()
        self.client.login(username='bob', password='pass')
        resp = self.client.get(reverse('ex:vote', args=[self.tip.id, -1]))
        self.assertTrue(Vote.objects.filter(tip=self.tip, user=self.bob, value=-1).exists())
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.reputation, -2)

    def test_delete_by_author(self):
        self.client.login(username='alice', password='pass')
        resp = self.client.get(reverse('ex:delete_tip', args=[self.tip.id]))
        self.assertFalse(Tip.objects.filter(pk=self.tip.id).exists())

    def test_delete_by_reputation(self):
        # bob gains reputation to delete others' tips
        self.bob.reputation = 30
        self.bob.save()
        self.client.login(username='bob', password='pass')
        resp = self.client.get(reverse('ex:delete_tip', args=[self.tip.id]))
        self.assertFalse(Tip.objects.filter(pk=self.tip.id).exists())

    def test_tip_deletion_removes_vote_influence(self):
        # create two voters and votes
        c1 = User.objects.create_user(username='c1', password='pass')
        c2 = User.objects.create_user(username='c2', password='pass')
        # cast votes via the view to ensure signals and permissions run
        self.client.force_login(c1)
        self.client.get(reverse('ex:vote', args=[self.tip.id, '1']))
        self.client.force_login(c2)
        # give c2 rep to be allowed to downvote
        c2.reputation = 15
        c2.save()
        self.client.get(reverse('ex:vote', args=[self.tip.id, '-1']))
        self.alice.refresh_from_db()
        # upvote +5, downvote -2 => net +3
        self.assertEqual(self.alice.reputation, 3)
        # delete tip should remove influence
        self.tip.delete()
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.reputation, 0)
from django.test import TestCase

# Create your tests here.
