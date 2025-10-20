from django.db import models
from django.contrib.auth import get_user_model
from common.models import SoftDeleteModel, TimestampedModel


class TextAnalysis(SoftDeleteModel, TimestampedModel):
    text = models.TextField(null=False)
    user = models.ForeignKey(
        get_user_model(), null=True, blank=True, on_delete=models.SET_NULL
    )
    summarized_text = models.TextField(null=True)
    extracted_metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"TextAnalysis(id={self.id}, user={self.user}, text={self.text[:30]}...)"

    class Meta:
        db_table = "text_analyses"
        verbose_name = "Text Analysis"
