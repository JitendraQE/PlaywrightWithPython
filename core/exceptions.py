"""Framework-specific exceptions."""


class FrameworkError(RuntimeError):
    """Base exception for framework-level failures."""


class ConfigurationError(FrameworkError):
    """Raised when framework configuration is invalid or incomplete."""
