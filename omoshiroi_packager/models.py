"""
Data models for the packages module.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .version import Version


@dataclass
class FileProperties:
    """Properties of a file in the package."""

    path: str
    size: int
    sha256: str
    sha512: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "path": self.path,
            "size": self.size,
            "sha256": self.sha256,
            "sha512": self.sha512,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> FileProperties:
        """Create from dictionary."""
        return cls(
            path=data["path"],
            size=data["size"],
            sha256=data["sha256"],
            sha512=data["sha512"],
        )


@dataclass
class Manifest:
    """Package manifest."""

    version: str
    channel: str
    timestamp: int = field(default_factory=lambda: int(time.time()))
    files: List[FileProperties] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "channel": self.channel,
            "timestamp": self.timestamp,
            "files": [f.to_dict() for f in self.files],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Manifest:
        """Create from dictionary."""
        files = [FileProperties.from_dict(f) for f in data.get("files", [])]
        return cls(
            version=data["version"],
            channel=data["channel"],
            timestamp=data.get("timestamp", int(time.time())),
            files=files,
        )

    @property
    def version_obj(self) -> Version:
        """Get Version object from version string."""
        from .version import parse

        return parse(self.version)


@dataclass
class UpdateCheckResult:
    """Result of an update check."""

    update_required: bool
    latest_version: Optional[str] = None
    current_version: Optional[str] = None
    error: Optional[str] = None

    @property
    def has_error(self) -> bool:
        """Whether there was an error."""
        return self.error is not None

    @classmethod
    def success(
        cls, update_required: bool, latest_version: str, current_version: str
    ) -> UpdateCheckResult:
        """Create a successful result."""
        return cls(
            update_required=update_required,
            latest_version=latest_version,
            current_version=current_version,
        )

    @classmethod
    def failure(cls, error: str) -> UpdateCheckResult:
        """Create a failure result."""
        return cls(
            update_required=False,
            error=error,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"update_required": self.update_required}
        if self.latest_version is not None:
            result["latest_version"] = self.latest_version
        if self.current_version is not None:
            result["current_version"] = self.current_version
        if self.error is not None:
            result["error"] = self.error
        return result
