from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

User = getattr(settings, 'AUTH_USER_MODEL')


class Question(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions',
        related_query_name='question'
    )
    content = models.CharField(max_length=240)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-updated']
        unique_together = ('content', 'slug')

    def __str__(self):
        return "Question: {}\nBy: {}".format(self.content, self.author.username)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('question-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.content
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(unique=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        related_query_name='answer'
    )
    voters = models.ManyToManyField(User, related_name='votes')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "Answer: {}\nBy: {}".format(self.body, self.author.username)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id
        }
        return reverse('answer-detail', kwargs=kwargs)

