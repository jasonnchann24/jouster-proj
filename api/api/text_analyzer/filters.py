import django_filters
from .models import TextAnalysis


class TopicFilter(django_filters.FilterSet):
    topics = django_filters.CharFilter(
        field_name="extracted_metadata__topics", lookup_expr="icontains", label="Topics"
    )

    class Meta:
        model = TextAnalysis
        fields = ["topics"]
