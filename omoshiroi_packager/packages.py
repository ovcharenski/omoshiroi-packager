"""
Main entry point for the packages module.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

from .config import Config
from .core import Packager, Updater

# Global config instance (lazy loaded)
_config: Optional[Config] = None


def get_config(load_dotenv: bool = True) -> Config:
    """
    Get or create the global config instance.

    Args:
        load_dotenv: Whether to load .env file

    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config.from_env(load_dotenv_file=load_dotenv)
        _config.ensure_directories()
    return _config


def reset_config() -> None:
    """Reset the global config instance."""
    global _config
    _config = None


def get_latest_version(channel: str, config: Optional[Config] = None) -> Optional[str]:
    """
    Get the latest version for a channel.

    Args:
        channel: Channel name (dev, alpha, beta, rc, stable, hotfix)
        config: Config instance (uses global if not provided)

    Returns:
        Latest version string or None

    Example:
        >>> get_latest_version("stable")
        '1.2.3'
    """
    if config is None:
        config = get_config()

    updater = Updater(config)
    return updater.get_latest_version(channel)


def check_update(
    current_version: str, channel: str = "stable", config: Optional[Config] = None
) -> dict:
    """
    Check if an update is available.

    Args:
        current_version: Current version string
        channel: Channel to check
        config: Config instance (uses global if not provided)

    Returns:
        Dictionary with update information:
            - update_required: bool
            - latest_version: str (if available)
            - current_version: str (if available)
            - error: str (if error occurred)

    Example:
        >>> check_update("1.0.0", "stable")
        {'update_required': True, 'latest_version': '1.2.3', 'current_version': '1.0.0'}
    """
    if config is None:
        config = get_config()

    updater = Updater(config)
    result = updater.check_update(current_version, channel)
    return result.to_dict()


def pack_version(
    version: Optional[str] = None, channel: Optional[str] = None, config: Optional[Config] = None
) -> Tuple[BytesIO, Path]:
    """
    Package a version.

    Args:
        version: Version string (reads from .config if not provided)
        channel: Channel name (parsed from version if not provided)
        config: Config instance (uses global if not provided)

    Returns:
        Tuple of (zip_data, manifest_path)

    Raises:
        PackError: If packaging fails

    Example:
        >>> zip_data, manifest_path = pack_version("1.0.0", "stable")
    """
    if config is None:
        config = get_config()

    packager = Packager(config)
    return packager.pack_version(version, channel)


def pack_by_channel(channel: str, config: Optional[Config] = None) -> Tuple[BytesIO, Path]:
    """
    Package the latest version for a channel.

    Args:
        channel: Channel name
        config: Config instance (uses global if not provided)

    Returns:
        Tuple of (zip_data, manifest_path)

    Raises:
        PackError: If packaging fails
    """
    if config is None:
        config = get_config()

    packager = Packager(config)
    return packager.pack_by_channel(channel)


def make_manifest(version: str, channel: str, config: Optional[Config] = None) -> str:
    """
    Create a manifest for a version.

    Args:
        version: Version string
        channel: Channel name
        config: Config instance (uses global if not provided)

    Returns:
        Path to created manifest

    Example:
        >>> make_manifest("1.0.0", "stable")
        '/path/to/manifest-stable.json'
    """
    if config is None:
        config = get_config()

    packager = Packager(config)
    manifest = packager.manifest_manager.create_manifest(version, channel)
    manifest_path = packager.manifest_manager.save_manifest(manifest, channel)
    return str(manifest_path)


def get_all_versions(config: Optional[Config] = None) -> dict:
    """
    Get versions from all channels.

    Args:
        config: Config instance (uses global if not provided)

    Returns:
        Dictionary mapping channel to version string

    Example:
        >>> get_all_versions()
        {'dev': '1.0.0-dev.1', 'alpha': None, 'beta': '1.2.3-beta.1', ...}
    """
    if config is None:
        config = get_config()

    updater = Updater(config)
    return updater.get_all_versions()


__all__ = [
    "check_update",
    "get_all_versions",
    "get_config",
    "get_latest_version",
    "make_manifest",
    "pack_by_channel",
    "pack_version",
    "reset_config",
]
