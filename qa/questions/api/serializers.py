from rest_framework import serializers
from qa.questions import models


class AnswerSerializer(serializers.ModelSerializer):
    # String repr of author field
    author = serializers.StringRelatedField(read_only=True)
    # Method field
    created = serializers.SerializerMethodField()
    # slug = serializers.SlugField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField()

    class Meta:
        model = models.Answer
        exclude = ["question", "voters", "updated"]

    def get_created(self, instance):
        # MM dd yyyy
        return instance.created.strftime("%B %d, %Y")

    def get_likes_count(self, instance):
        # MM dd yyyy
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()


class QuestionSerializer(serializers.ModelSerializer):
    # String repr of author field
    author = serializers.StringRelatedField(read_only=True)
    # Method field
    created = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    answers_count = serializers.SerializerMethodField()
    user_has_answered = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        exclude = ["updated"]

    def get_created(self, instance):
        # MM dd yyyy
        return instance.created.strftime("%B %d, %Y")

    def get_answers_count(self, instance):
        # Related name from the Answer's model question field
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        return instance.answers.filter(author=request.user).exists()




