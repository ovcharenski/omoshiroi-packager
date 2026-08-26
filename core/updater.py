"""
Update checking functionality for the packages module.
"""

from typing import Optional, List

from ..config import Config
from ..models import UpdateCheckResult
from ..exceptions import VersionError
from ..version import parse, Version
from .manifest import ManifestManager


class Updater:
    """Handler for checking updates."""
    
    # Channel priority order
    CHANNEL_ORDER = ["dev", "alpha", "beta", "rc", "stable", "hotfix"]
    
    def __init__(self, config: Config):
        """
        Initialize updater.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.manifest_manager = ManifestManager(config)
    
    def get_latest_version(self, channel: str) -> Optional[str]:
        """
        Get the latest version for a channel.
        
        For 'stable': returns stable version directly.
        For other channels: returns the latest version among all channels
        up to and including the specified channel.
        
        Args:
            channel: Channel name
            
        Returns:
            Latest version string or None
        """
        if channel == "stable":
            return self.manifest_manager.get_version("stable")
        
        # Get all versions up to the specified channel
        try:
            channel_index = self.CHANNEL_ORDER.index(channel)
        except ValueError:
            raise VersionError(f"Invalid channel: {channel}")
        
        channels_to_check = self.CHANNEL_ORDER[:channel_index + 1]
        
        versions = []
        for ch in channels_to_check:
            version_str = self.manifest_manager.get_version(ch)
            if version_str is not None:
                versions.append(parse(version_str))
        
        if not versions:
            return None
        
        # Return the latest version
        return str(max(versions))
    
    def check_update(self, current_version: str, channel: str = "stable") -> UpdateCheckResult:
        """
        Check if an update is available.
        
        Args:
            current_version: Current version string
            channel: Channel to check
            
        Returns:
            UpdateCheckResult object
        """
        try:
            # Parse current version
            current = parse(current_version)
            
            # Get latest version
            latest_str = self.get_latest_version(channel)
            
            if latest_str is None:
                return UpdateCheckResult.failure("No version found for channel")
            
            latest = parse(latest_str)
            
            # Compare versions
            update_required = current < latest
            
            return UpdateCheckResult.success(
                update_required=update_required,
                latest_version=latest_str,
                current_version=current_version,
            )
            
        except Exception as e:
            return UpdateCheckResult.failure(str(e))
    
    def get_all_versions(self) -> dict:
        """
        Get versions from all channels.
        
        Returns:
            Dictionary mapping channel to version string
        """
        result = {}
        for channel in self.CHANNEL_ORDER:
            result[channel] = self.manifest_manager.get_version(channel)
        return result
    
    def get_latest_stable(self) -> Optional[str]:
        """Get the latest stable version."""
        return self.manifest_manager.get_version("stable")
    
    def get_latest_prerelease(self) -> Optional[str]:
        """Get the latest pre-release version."""
        prerelease_channels = ["dev", "alpha", "beta", "rc"]
        
        versions = []
        for channel in prerelease_channels:
            version_str = self.manifest_manager.get_version(channel)
            if version_str is not None:
                versions.append(parse(version_str))
        
        if not versions:
            return None
        
        return str(max(versions))
    
    def is_newer_than_stable(self, channel: str) -> bool:
        """
        Check if a channel's version is newer than stable.
        
        Args:
            channel: Channel to check
            
        Returns:
            True if channel version is newer than stable
        """
        stable = self.manifest_manager.get_version("stable")
        channel_version = self.manifest_manager.get_version(channel)
        
        if stable is None or channel_version is None:
            return False
        
        return parse(channel_version) > parse(stable)
    
    def clear_cache(self) -> None:
        """Clear the cache."""
        self.manifest_manager.clear_cache()