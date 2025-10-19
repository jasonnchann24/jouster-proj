from api.text_analyzer.services import extract_top_nouns
from django.conf import settings
from openai import OpenAI
from api.text_analyzer.protocols.llm_protocol import ExtractedData
from rest_framework.exceptions import APIException


class OpenAIException(APIException):
    status_code = 502
    default_detail = "Error communicating with OpenAI API."
    default_code = "openai_error"


class OpenAIStrategy:
    extracted_meta = ExtractedData(
        summarized_text="", title="", topics=[], sentiment="", keywords=[]
    )

    def summarize(self, text: str) -> str:
        res = self._call_api(text)
        self.extracted_meta.summarized_text = res.summarized_text
        self.extracted_meta.title = res.title
        self.extracted_meta.topics = res.topics
        self.extracted_meta.sentiment = res.sentiment
        self.extracted_meta.keywords = extract_top_nouns(text, top_n=3)

        return res.summarized_text

    def get_extracted_metadata(self) -> ExtractedData:
        return self.extracted_meta

    def _call_api(self, text: str) -> ExtractedData:
        if settings.OPEN_AI_KEY is None or settings.OPEN_AI_KEY == "":
            return self.__mock_data()

        client = OpenAI(api_key=settings.OPEN_AI_KEY)
        try:
            response = client.responses.parse(
                model="gpt-4.1-nano",
                input=[
                    {
                        "role": "developer",
                        "content": "Read the user content fully then summarize the text in 1-2 sentences, maximum 15 words per sentence. Extract title, 3 key topics, and positive / neutral / negative sentiment.",
                    },
                    {"role": "user", "content": text},
                ],
                text_format=ExtractedData,
            )
            output = response.output_parsed
            return output
        except Exception:
            raise OpenAIException()

    def __mock_data(self) -> ExtractedData:
        return ExtractedData(
            summarized_text="Mock - This is a summarized version of the text.",
            title="Mock - Summarized Title",
            topics=["Mock - Topic1", "Mock - Topic2"],
            sentiment="positive",
            keywords=[],
        )
