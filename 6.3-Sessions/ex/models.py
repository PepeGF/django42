from django.db import models

class Tips(models.Model):
    content = models.TextField(null=False, blank=False)
    author = models.CharField(max_length=150, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:30]}..."