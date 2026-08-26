"""
Custom exceptions for the packages module.
"""


class PackageError(Exception):
    """Base exception for package-related errors."""



class ManifestError(PackageError):
    """Exception raised for manifest errors."""



class FileError(PackageError):
    """Exception raised for file-related errors."""



class HashError(PackageError):
    """Exception raised for hash generation errors."""



class VersionError(PackageError):
    """Exception raised for version-related errors."""



class ConfigError(PackageError):
    """Exception raised for configuration errors."""



class PackError(PackageError):
    """Exception raised for packaging errors."""

