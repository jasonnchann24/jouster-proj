from typing import Protocol

from pydantic import BaseModel


class ExtractedData(BaseModel):
    summarized_text: str
    title: str
    topics: list[str]
    sentiment: str
    keywords: list[str]


class LLMStrategy(Protocol):
    def summarize(self, text: str) -> str: ...
    def get_extracted_metadata(self) -> ExtractedData: ...
