"""
Manifest management for the packages module.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import Config
from ..models import FileProperties, Manifest
from ..exceptions import ManifestError
from ..utils.file_utils import ProjectFiles
from ..utils.hash_utils import generate_file_hash


class ManifestManager:
    """Manager for package manifests."""

    def __init__(self, config: Config):
        """
        Initialize manifest manager.

        Args:
            config: Application configuration
        """
        self.config = config
        self._cache: Dict[str, Optional[Manifest]] = {}

    def create_manifest(
        self,
        version: str,
        channel: str,
        project_files: Optional[ProjectFiles] = None,
    ) -> Manifest:
        """
        Create a new manifest for a version.

        Args:
            version: Version string
            channel: Channel name
            project_files: ProjectFiles instance (creates new if not provided)

        Returns:
            Manifest object
        """
        if project_files is None:
            project_files = ProjectFiles(self.config.project_dir)

        files_list = []
        for file_path in project_files.get_files():
            full_path = project_files.get_full_path(file_path)

            if full_path.exists():
                sha256, sha512 = generate_file_hash(full_path)
                files_list.append(
                    FileProperties(
                        path=file_path,
                        size=full_path.stat().st_size,
                        sha256=sha256,
                        sha512=sha512,
                    )
                )

        return Manifest(
            version=version,
            channel=channel,
            timestamp=int(time.time()),
            files=files_list,
        )

    def save_manifest(self, manifest: Manifest, channel: Optional[str] = None) -> Path:
        """
        Save a manifest to disk.

        Args:
            manifest: Manifest object
            channel: Channel name (uses manifest.channel if not provided)

        Returns:
            Path to saved manifest file
        """
        channel = channel or manifest.channel
        manifest_path = self.config.get_manifest_path(channel)

        # Ensure manifest directory exists
        manifest_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest.to_dict(), f, indent=2)
        except OSError as e:
            raise ManifestError(f"Failed to save manifest {manifest_path}: {e}")

        return manifest_path

    def load_manifest(self, channel: str) -> Optional[Manifest]:
        """
        Load a manifest from disk.

        Args:
            channel: Channel name

        Returns:
            Manifest object or None if not found
        """
        # Check cache
        if channel in self._cache:
            return self._cache[channel]

        manifest_path = self.config.get_manifest_path(channel)

        if not manifest_path.exists():
            return None

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            manifest = Manifest.from_dict(data)
            self._cache[channel] = manifest
            return manifest

        except (OSError, json.JSONDecodeError) as e:
            raise ManifestError(f"Failed to load manifest {manifest_path}: {e}")

    def get_version(self, channel: str) -> Optional[str]:
        """
        Get version from a channel's manifest.

        Args:
            channel: Channel name

        Returns:
            Version string or None
        """
        manifest = self.load_manifest(channel)
        return manifest.version if manifest else None

    def get_all_manifests(self) -> Dict[str, Optional[Manifest]]:
        """
        Get manifests for all channels.

        Returns:
            Dictionary mapping channel to Manifest
        """
        # Channels list - can be extended
        channels = ["dev", "alpha", "beta", "rc", "stable", "hotfix"]

        result = {}
        for channel in channels:
            result[channel] = self.load_manifest(channel)

        return result

    def clear_cache(self) -> None:
        """Clear the manifest cache."""
        self._cache.clear()
