from rest_framework import serializers

from qa.questions.models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    # String repr of author field
    author = serializers.StringRelatedField(read_only=True)
    # Method field
    created = serializers.DateTimeField(format="%B %d, %Y", read_only=True)
    # slug = serializers.SlugField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField()
    question_slug = serializers.SerializerMethodField()
    # def get_created(self, instance):
    #     # MM dd yyyy
    #     return instance.created.strftime("%B %d, %Y")

    def get_likes_count(self, instance):
        # MM dd yyyy
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_question_slug(self, instance):
        return instance.question.slug
        
    class Meta:
        model = Answer
        # fields = ['author', 'body', 'created', 'likes_count', 'user_has_voted', 'url']
        exclude = ["question", "voters", "updated"]
       
    



class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created = serializers.DateTimeField(format="%B %d, %Y", read_only=True)
    answers_count = serializers.SerializerMethodField()
    user_has_answered = serializers.SerializerMethodField()

    def get_answers_count(self, instance):
            # Related name from the Answer's model question field
            return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        return instance.answers.filter(author=request.user).exists()

    class Meta:
        model = Question
        fields = ["author", "content", "slug","created", "answers_count", "user_has_answered", "url"]
       

        extra_kwargs = {
            "url": {"view_name": "api:question-detail", "lookup_field": "slug"}
        }
        
       
        