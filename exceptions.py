"""
Custom exceptions for the packages module.
"""


class PackageError(Exception):
    """Base exception for package-related errors."""
    pass


class ManifestError(PackageError):
    """Exception raised for manifest errors."""
    pass


class FileError(PackageError):
    """Exception raised for file-related errors."""
    pass


class HashError(PackageError):
    """Exception raised for hash generation errors."""
    pass


class VersionError(PackageError):
    """Exception raised for version-related errors."""
    pass


class ConfigError(PackageError):
    """Exception raised for configuration errors."""
    pass


class PackError(PackageError):
    """Exception raised for packaging errors."""
    pass