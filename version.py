"""
Version parser for Python packages.

Supports format: X.X.x.x-[channel].X.x.x

Where:
    X - required digit
    x - optional digit

Channels (in order from earliest to latest):
    dev < alpha < beta < rc < stable < hotfix
"""

import re
from typing import Optional, Tuple, Dict, Any, List


class InvalidVersion(ValueError):
    """Exception raised for invalid version strings."""
    pass


class Version:
    """Version class with support for multiple channels."""
    
    __slots__ = (
        "_major", "_minor", "_patch", "_build",
        "_channel", "_channel_major", "_channel_minor", "_channel_patch",
        "_key_cache", "_string_cache"
    )
    
    _CHANNEL_ORDER = {
        "dev": 0,
        "alpha": 1,
        "beta": 2,
        "rc": 3,
        "stable": 4,
        "hotfix": 5,
    }
    
    _VALID_CHANNELS = frozenset(_CHANNEL_ORDER.keys())
    
    _PATTERN = re.compile(
        r"^(\d+)\.(\d+)(?:\.(\d+))?(?:\.(\d+))?"
        r"(?:-(dev|alpha|beta|rc|stable|hotfix)\.(\d+)(?:\.(\d+))?(?:\.(\d+))?)?$"
    )
    
    def __init__(self, version: str) -> None:
        match = self._PATTERN.match(version.strip())
        if not match:
            raise InvalidVersion(
                f"Invalid version format: '{version}'. "
                f"Expected: X.X[.x][.x][-channel.X[.x][.x]]"
            )
        
        groups = match.groups()
        
        self._major = int(groups[0])
        self._minor = int(groups[1])
        self._patch = int(groups[2]) if groups[2] is not None else 0
        self._build = int(groups[3]) if groups[3] is not None else 0
        
        if groups[4] is None:
            self._channel = "stable"
            self._channel_major = 0
            self._channel_minor = 0
            self._channel_patch = 0
        else:
            channel = groups[4]
            if channel not in self._VALID_CHANNELS:
                raise InvalidVersion(f"Invalid channel '{channel}'")
            
            self._channel = channel
            self._channel_major = int(groups[5])
            self._channel_minor = int(groups[6]) if groups[6] is not None else 0
            self._channel_patch = int(groups[7]) if groups[7] is not None else 0
        
        self._key_cache = None
        self._string_cache = None
    
    # Properties
    @property
    def major(self) -> int:
        return self._major
    
    @property
    def minor(self) -> int:
        return self._minor
    
    @property
    def patch(self) -> int:
        return self._patch
    
    @property
    def build(self) -> int:
        return self._build
    
    @property
    def channel(self) -> str:
        return self._channel
    
    @property
    def channel_order(self) -> int:
        return self._CHANNEL_ORDER[self._channel]
    
    @property
    def channel_major(self) -> int:
        return self._channel_major
    
    @property
    def channel_minor(self) -> int:
        return self._channel_minor
    
    @property
    def channel_patch(self) -> int:
        return self._channel_patch
    
    @property
    def channel_version(self) -> Tuple[int, int, int]:
        return (self._channel_major, self._channel_minor, self._channel_patch)
    
    @property
    def is_dev(self) -> bool:
        return self._channel == "dev"
    
    @property
    def is_alpha(self) -> bool:
        return self._channel == "alpha"
    
    @property
    def is_beta(self) -> bool:
        return self._channel == "beta"
    
    @property
    def is_rc(self) -> bool:
        return self._channel == "rc"
    
    @property
    def is_stable(self) -> bool:
        return self._channel == "stable"
    
    @property
    def is_hotfix(self) -> bool:
        return self._channel == "hotfix"
    
    @property
    def is_prerelease(self) -> bool:
        return self._channel in ("dev", "alpha", "beta", "rc")
    
    @property
    def is_release(self) -> bool:
        return self._channel in ("stable", "hotfix")
    
    @property
    def base_version(self) -> str:
        parts = [str(self._major), str(self._minor)]
        if self._patch != 0 or self._build != 0:
            parts.append(str(self._patch))
        if self._build != 0:
            parts.append(str(self._build))
        return ".".join(parts)
    
    @property
    def full_version(self) -> str:
        return f"{self._major}.{self._minor}.{self._patch}.{self._build}"
    
    @property
    def _key(self) -> tuple:
        if self._key_cache is None:
            self._key_cache = (
                self._major,
                self._minor,
                self._patch,
                self._build,
                self._CHANNEL_ORDER[self._channel],
                self._channel_major,
                self._channel_minor,
                self._channel_patch,
            )
        return self._key_cache
    
    # Comparison
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._key == other._key
    
    def __lt__(self, other: Version) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._key < other._key
    
    def __le__(self, other: Version) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._key <= other._key
    
    def __gt__(self, other: Version) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._key > other._key
    
    def __ge__(self, other: Version) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._key >= other._key
    
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._key != other._key
    
    def __hash__(self) -> int:
        return hash(self._key)
    
    # String representation
    def __str__(self) -> str:
        if self._string_cache is None:
            parts = [str(self._major), str(self._minor)]
            if self._patch != 0 or self._build != 0:
                parts.append(str(self._patch))
            if self._build != 0:
                parts.append(str(self._build))
            base = ".".join(parts)
            
            if self._channel != "stable":
                suffix = f"-{self._channel}.{self._channel_major}"
                if self._channel_minor != 0:
                    suffix += f".{self._channel_minor}"
                if self._channel_patch != 0:
                    suffix += f".{self._channel_patch}"
                self._string_cache = base + suffix
            else:
                self._string_cache = base
        
        return self._string_cache
    
    def __repr__(self) -> str:
        return f"<Version('{self}')>"
    
    # Version manipulation
    def promote(self) -> "Version":
        channels = ["dev", "alpha", "beta", "rc", "stable", "hotfix"]
        current_idx = channels.index(self._channel)
        
        if current_idx < len(channels) - 1:
            next_channel = channels[current_idx + 1]
            return Version(f"{self.full_version}-{next_channel}.1")
        
        return self
    
    def demote(self) -> "Version":
        channels = ["dev", "alpha", "beta", "rc", "stable", "hotfix"]
        current_idx = channels.index(self._channel)
        
        if current_idx > 0:
            prev_channel = channels[current_idx - 1]
            return Version(f"{self.full_version}-{prev_channel}.1")
        
        return self
    
    def next_patch(self) -> "Version":
        return Version(f"{self._major}.{self._minor}.{self._patch + 1}")
    
    def next_minor(self) -> "Version":
        return Version(f"{self._major}.{self._minor + 1}.0")
    
    def next_major(self) -> "Version":
        return Version(f"{self._major + 1}.0.0")
    
    def with_build(self, build: int) -> "Version":
        base = f"{self._major}.{self._minor}.{self._patch}.{build}"
        if self._channel != "stable":
            suffix = f"-{self._channel}.{self._channel_major}"
            if self._channel_minor != 0:
                suffix += f".{self._channel_minor}"
            if self._channel_patch != 0:
                suffix += f".{self._channel_patch}"
            return Version(base + suffix)
        return Version(base)
    
    def with_channel(self, channel: str) -> "Version":
        if channel not in self._VALID_CHANNELS:
            raise ValueError(f"Invalid channel: {channel}")
        
        if channel == "stable":
            return Version(self.full_version)
        
        return Version(f"{self.full_version}-{channel}.1")
    
    def get_stable_version(self) -> "Version":
        return Version(self.full_version)
    
    # Serialization
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "major": self._major,
            "minor": self._minor,
            "patch": self._patch,
            "build": self._build,
            "channel": self._channel,
            "channel_order": self.channel_order,
            "is_prerelease": self.is_prerelease,
            "is_release": self.is_release,
            "base_version": self.base_version,
            "full_version": self.full_version,
            "string": str(self),
        }
        
        if self._channel != "stable":
            result["channel_version"] = {
                "major": self._channel_major,
                "minor": self._channel_minor,
                "patch": self._channel_patch,
            }
        
        return result
    
    def to_tuple(self) -> tuple:
        return (
            self._major,
            self._minor,
            self._patch,
            self._build,
            self._channel,
            self._channel_major,
            self._channel_minor,
            self._channel_patch,
        )
    
    @classmethod
    def from_tuple(cls, data: tuple) -> "Version":
        major, minor, patch, build, channel, ch_major, ch_minor, ch_patch = data
        
        version = f"{major}.{minor}"
        if patch != 0 or build != 0:
            version += f".{patch}"
        if build != 0:
            version += f".{build}"
        
        if channel != "stable":
            version += f"-{channel}.{ch_major}"
            if ch_minor != 0:
                version += f".{ch_minor}"
            if ch_patch != 0:
                version += f".{ch_patch}"
        
        return cls(version)
    
    @classmethod
    def valid_channels(cls) -> List[str]:
        return list(cls._CHANNEL_ORDER.keys())


# Public API
def parse(version: str) -> Version:
    """Parse a version string into a Version object."""
    return Version(version)


def is_valid(version: str) -> bool:
    """Check if version string is valid."""
    try:
        Version(version)
        return True
    except InvalidVersion:
        return False


def sort_versions(versions: List[str]) -> List[str]:
    """Sort version strings in ascending order."""
    return sorted(versions, key=parse)


def latest_version(versions: List[str]) -> Optional[str]:
    """Get the latest version from a list."""
    if not versions:
        return None
    return max(versions, key=parse)


def latest_stable(versions: List[str]) -> Optional[str]:
    """Get the latest stable version from a list."""
    stable = [v for v in versions if parse(v).is_stable]
    if not stable:
        return None
    return max(stable, key=parse)