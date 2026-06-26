class LLMServiceError(Exception):
    def __init__(
        self,
        code: str = "LLM_SERVICE_ERROR",
        message: str = "LLM service is temporarily unavailable",
    ):
        self.code = code
        self.message = message