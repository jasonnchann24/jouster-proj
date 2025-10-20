from rest_framework import serializers
from .models import TextAnalysis
from user_accounts.serializers import UserSerializer
from .strategies.OpenAIStrategy import OpenAIStrategy
from .managers.llm_manager import LLMManager


# TRANSFORMERS
class TextAnalysisSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        if hasattr(obj, "user") and obj.user is not None:
            return UserSerializer(obj.user, context=self.context).data
        return None

    class Meta:
        model = TextAnalysis
        fields = [
            "id",
            "user_id",
            "text",
            "summarized_text",
            "extracted_metadata",
            "user",
            "created_at",
        ]
        read_only_fields = ["id"]


# REQUEST SERIALIZERS
class TextAnalysisCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextAnalysis
        fields = [
            "text",
        ]

    def validate(self, data):
        if not data.get("text"):
            raise serializers.ValidationError("Text field cannot be empty.")

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["user"] = request.user

        chosen_strategy = OpenAIStrategy()
        llm_manager = LLMManager(chosen_strategy)

        text = self.validated_data.get("text", "")
        summarized_text = llm_manager.summarize(text)

        validated_data["summarized_text"] = summarized_text
        validated_data["extracted_metadata"] = llm_manager.get_metadata().model_dump(
            exclude={"summarized_text"}
        )

        return super().create(validated_data)
