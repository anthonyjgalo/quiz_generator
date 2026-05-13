class DocumentLinkedError(Exception):
    """Raised when trying to delete a document linked to a quiz."""

    pass


class EmptyWorkspaceError(Exception):
    """Raised when trying to leave a workspace with 0 documents."""

    pass


class QuestionLimitError(Exception):
    """Raised when requesting too many questions for a short context."""

    pass


class InsufficientContextError(Exception):
    """Raised when no relevant context is retrieved for quiz generation."""

    pass


class ConnectionTestFailed(Exception):
    """Raised when a connection test to an LLM provider fails.

    This exception wraps underlying errors (API errors, timeouts, network issues)
    into a single domain-specific exception for the connection layer.
    """

    pass
