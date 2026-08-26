"""
Omoshiroi Packager - Version management and packaging utilities.

A comprehensive package for parsing, comparing, and managing software versions
with multiple channel support (dev, alpha, beta, rc, stable, hotfix).
"""

from .config import Config
from .core import ManifestManager, Packager, Updater
from .exceptions import (
    ConfigError,
    FileError,
    HashError,
    ManifestError,
    PackageError,
    PackError,
    VersionError,
)
from .models import FileProperties, Manifest, UpdateCheckResult
from .packages import (
    check_update,
    get_all_versions,
    get_latest_version,
    make_manifest,
    pack_by_channel,
    pack_version,
    reset_config,
)
from .utils import (
    IgnorePattern,
    ProjectConfig,
    ProjectFiles,
    create_zip_from_files,
    extract_zip,
    generate_file_hash,
    get_zip_file_list,
    verify_file_hash,
)
from .version import (
    InvalidVersion,  # ← ДОБАВИТЬ ЭТО
    Version,
    is_valid,
    latest_stable,
    latest_version,
    parse,
    sort_versions,
)

__version__ = "0.1.1"
__author__ = "ovcharenski"

__all__ = [
    # Version
    "InvalidVersion",  # ← ДОБАВИТЬ ЭТО
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
    "pack_by_channel",
    "make_manifest",
    "get_all_versions",
    "reset_config",
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