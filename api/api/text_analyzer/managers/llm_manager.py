from api.text_analyzer.protocols.llm_protocol import LLMStrategy, ExtractedData


class LLMManager:
    """Manages LLM Strategy that you want to use"""

    def __init__(self, strategy: LLMStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: LLMStrategy):
        """Swap strategy"""
        self._strategy = strategy

    def summarize(self, text: str) -> str:
        """Summarize text using the selected strategy"""
        return self._strategy.summarize(text)

    def get_metadata(self) -> ExtractedData:
        """Get extracted metadata using the selected strategy"""
        return self._strategy.get_extracted_metadata()
