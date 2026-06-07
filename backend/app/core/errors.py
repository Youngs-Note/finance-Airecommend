class ApplicationError(Exception):
    """Base class for expected application errors."""


class ConfigurationError(ApplicationError):
    """Raised when required environment settings are missing."""


class ExternalApiError(ApplicationError):
    """Raised when an external API request cannot be completed."""


class ProductNotFoundError(ApplicationError):
    """Raised when a product cannot be found."""
