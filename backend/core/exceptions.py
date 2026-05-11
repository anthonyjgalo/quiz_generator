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
