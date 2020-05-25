from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from qa.questions.api.permissions import IsAuthorOrReadOnly
from qa.questions.api import serializers
from qa.questions import models


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all().order_by("-created")
    # Look up for editing, can be other field such as pk
    lookup_field = "slug"
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    # Added author to add automatically
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(models.Question, slug=kwarg_slug)

        if question.answers.filter(author=request_user).exists():
            raise ValidationError(_("You have already answered this question!"))

        serializer.save(author=request_user, question=question)


answer_create_view = AnswerCreateAPIView.as_view()


class AnswerListAPIView(generics.ListAPIView):
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return models.Answer.objects.filter(question__slug=kwarg_slug).order_by("-created")


answer_list_view = AnswerListAPIView.as_view()


class AnswerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


answer_rud_view = AnswerRetrieveUpdateDestroyAPIView.as_view()


class AnswerLikeAPIView(APIView):
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]

    # Post like
    def post(self, request, pk):
        answer = get_object_or_404(models.Answer, pk=pk)
        user = request.user

        answer.voters.add(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete like
    def delete(self, request, pk):
        answer = get_object_or_404(models.Answer, pk=pk)
        user = request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


answer_like_view = AnswerLikeAPIView.as_view()



