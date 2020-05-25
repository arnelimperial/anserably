from django.contrib import admin
from qa.questions import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'slug', 'created', 'updated')


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'body', 'question', 'created', 'updated')


