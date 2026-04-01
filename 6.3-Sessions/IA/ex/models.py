from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum


class User(AbstractUser):
	reputation = models.IntegerField(default=0)

	def can_downvote(self):
		return self.reputation >= 15

	def can_delete_tips(self):
		return self.reputation >= 30

	def __str__(self):
		return f"{self.username} ({self.reputation})"


class Tip(models.Model):
	content = models.TextField()
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def upvotes(self):
		return self.votes.filter(value=1).count()

	def downvotes(self):
		return self.votes.filter(value=-1).count()

	def score(self):
		return self.votes.aggregate(Sum('value'))['value__sum'] or 0

	def __str__(self):
		return f"Tip({self.pk}) by {self.author}"

	class Meta:
		permissions = [
			("can_downvote", "Can downvote tips (reputation-based)"),
		]


class Vote(models.Model):
	tip = models.ForeignKey(Tip, related_name='votes', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	value = models.IntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')])

	class Meta:
		unique_together = ('tip', 'user')

	def __str__(self):
		return f"Vote({self.value}) by {self.user} on Tip({self.tip_id})"


# Signals to maintain reputation
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver


@receiver(pre_save, sender=Vote)
def vote_pre_save(sender, instance, **kwargs):
	# store previous value for update handling
	if instance.pk:
		try:
			prev = Vote.objects.get(pk=instance.pk)
			instance._prev_value = prev.value
		except Vote.DoesNotExist:
			instance._prev_value = None
	else:
		instance._prev_value = None


@receiver(post_save, sender=Vote)
def vote_post_save(sender, instance, created, **kwargs):
	author = instance.tip.author
	if created:
		if instance.value == 1:
			author.reputation = models.F('reputation') + 5
		else:
			author.reputation = models.F('reputation') - 2
		author.save()
	else:
		prev = getattr(instance, '_prev_value', None)
		if prev is None:
			return
		if prev == instance.value:
			return
		# changed vote: adjust accordingly
		if prev == 1 and instance.value == -1:
			# remove +5, add -2 => net -7
			author.reputation = models.F('reputation') - 7
		elif prev == -1 and instance.value == 1:
			# remove -2, add +5 => net +7
			author.reputation = models.F('reputation') + 7
		author.save()


@receiver(post_delete, sender=Vote)
def vote_post_delete(sender, instance, **kwargs):
	author = instance.tip.author
	if instance.value == 1:
		author.reputation = models.F('reputation') - 5
	else:
		author.reputation = models.F('reputation') + 2
	author.save()



