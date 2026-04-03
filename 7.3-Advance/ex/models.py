from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False, related_name='articles')
    created = models.DateTimeField(auto_now_add=True)
    synopsis = models.CharField(max_length=312, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.title

class UserFavouriteArticle(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False, related_name='favourite_articles')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False, related_name='favourited_by')

    def __str__(self):
        return self.article.title

    # para ex06
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_user_article')
        ]