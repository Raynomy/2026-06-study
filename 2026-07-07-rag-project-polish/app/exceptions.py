class RAGServiceError(Exception):
    def __init__(
        self,
        code: str = "RAG_SERVICE_ERROR",
        message: str = "RAG service is temporarily unavailable",
    ):
        self.code = code
        self.message = message