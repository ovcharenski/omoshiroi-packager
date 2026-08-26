"""
Omoshiroi Packager - Version management and packaging utilities.

A comprehensive package for parsing, comparing, and managing software versions
with multiple channel support (dev, alpha, beta, rc, stable, hotfix).
"""

from .version import Version, parse, is_valid, sort_versions, latest_version, latest_stable
from .config import Config
from .models import Manifest, FileProperties, UpdateCheckResult
from .exceptions import (
    PackageError,
    ManifestError,
    FileError,
    HashError,
    VersionError,
    ConfigError,
    PackError,
)
from .packages import (
    get_latest_version,
    check_update,
    pack_version,
    make_manifest,
)

# Core classes for advanced usage
from .core.manifest import ManifestManager
from .core.packager import Packager
from .core.updater import Updater

# Utility functions
from .utils.file_utils import IgnorePattern, ProjectFiles, ProjectConfig
from .utils.hash_utils import generate_file_hash, verify_file_hash
from .utils.zip_utils import create_zip_from_files, extract_zip, get_zip_file_list

__version__ = "0.1.0"
__author__ = "ovcharenski"

__all__ = [
    # Version
    "Version",
    "parse",
    "is_valid",
    "sort_versions",
    "latest_version",
    "latest_stable",
    
    # Config
    "Config",
    
    # Models
    "Manifest",
    "FileProperties",
    "UpdateCheckResult",
    
    # Exceptions
    "PackageError",
    "ManifestError",
    "FileError",
    "HashError",
    "VersionError",
    "ConfigError",
    "PackError",
    
    # Main API
    "get_latest_version",
    "check_update",
    "pack_version",
    "make_manifest",
    
    # Core
    "ManifestManager",
    "Packager",
    "Updater",
    
    # Utils
    "IgnorePattern",
    "ProjectFiles",
    "ProjectConfig",
    "generate_file_hash",
    "verify_file_hash",
    "create_zip_from_files",
    "extract_zip",
    "get_zip_file_list",
]