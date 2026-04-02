from django.db import models
from django.contrib.auth.models import User

class Tips(models.Model):
    content = models.TextField(null=False, blank=False)
    author = models.CharField(max_length=150, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    # Many-to-many relations to track which users upvoted or downvoted a tip
    upvoters = models.ManyToManyField(User, related_name='upvoted_tips', blank=True)
    downvoters = models.ManyToManyField(User, related_name='downvoted_tips', blank=True)

    def __str__(self):
        return f"{self.author} - {self.content[:30]}..."

    @property
    def upvotes_count(self):
        return self.upvoters.count()

    @property
    def downvotes_count(self):
        return self.downvoters.count()