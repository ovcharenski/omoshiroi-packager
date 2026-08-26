"""
Packaging functionality for the packages module.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

from ..config import Config
from ..exceptions import PackError
from ..utils.file_utils import ProjectFiles, ProjectConfig
from ..utils.zip_utils import create_zip_from_files
from ..version import parse
from .manifest import ManifestManager


class Packager:
    """Handler for packaging versions."""

    def __init__(self, config: Config):
        """
        Initialize packager.

        Args:
            config: Application configuration
        """
        self.config = config
        self.manifest_manager = ManifestManager(config)

    def pack_version(
        self,
        version: Optional[str] = None,
        channel: Optional[str] = None,
    ) -> Tuple[BytesIO, Path]:
        """
        Package a version.

        Args:
            version: Version string (reads from .config if not provided)
            channel: Channel name (parsed from version if not provided)

        Returns:
            Tuple of (zip_data, manifest_path)

        Raises:
            PackError: If packaging fails
        """
        try:
            # Get version from config if not provided
            if version is None:
                project_config = ProjectConfig(self.config.get_config_file_path())
                version = project_config.get_version()

                if version is None:
                    raise PackError("Version not found in .config file")

            # Parse channel from version if not provided
            if channel is None:
                version_obj = parse(version)
                channel = version_obj.channel

            # Create project files handler
            project_files = ProjectFiles(self.config.project_dir)

            # Create manifest
            manifest = self.manifest_manager.create_manifest(
                version=version,
                channel=channel,
                project_files=project_files,
            )

            # Save manifest
            manifest_path = self.manifest_manager.save_manifest(manifest, channel)

            # Get files to zip
            files = project_files.get_files()

            # Create ZIP archive
            zip_data = create_zip_from_files(
                files=files,
                base_dir=self.config.project_dir,
                manifest_path=manifest_path,
            )

            return zip_data, manifest_path

        except Exception as e:
            raise PackError(f"Failed to pack version: {e}")

    def pack_by_channel(self, channel: str) -> Tuple[BytesIO, Path]:
        """
        Package the latest version for a channel.

        Args:
            channel: Channel name

        Returns:
            Tuple of (zip_data, manifest_path)
        """
        # Get version from manifest
        version = self.manifest_manager.get_version(channel)

        if version is None:
            raise PackError(f"No version found for channel: {channel}")

        return self.pack_version(version, channel)
