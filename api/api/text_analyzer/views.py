from rest_framework import viewsets, permissions, mixins
from .models import TextAnalysis
from .serializers import TextAnalysisSerializer, TextAnalysisCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TopicFilter


class TextAnalysisMixins(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = TextAnalysis.objects.select_related("user").order_by("-created_at").all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TopicFilter

    def get_serializer_class(self):
        if self.action == "create":
            return TextAnalysisCreateSerializer
        return TextAnalysisSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = TextAnalysisSerializer(
            instance, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
