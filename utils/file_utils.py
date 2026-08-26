"""
File utilities for the packages module.
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Pattern

from ..exceptions import FileError


class IgnorePattern:
    """Handler for .ignore file patterns."""
    
    def __init__(self, patterns: List[str]):
        """
        Initialize with patterns.
        
        Args:
            patterns: List of ignore patterns (supports * wildcards)
        """
        self.patterns = [self._compile_pattern(p) for p in patterns]
    
    @staticmethod
    def _compile_pattern(pattern: str) -> Pattern:
        """Compile a glob pattern to regex."""
        # Escape special regex characters except *
        regex_pattern = re.escape(pattern).replace("\\*", ".*")
        return re.compile(f"^{regex_pattern}$")
    
    def is_ignored(self, file_path: str) -> bool:
        """
        Check if a file path matches any ignore pattern.
        
        Args:
            file_path: File path to check
            
        Returns:
            True if file should be ignored
        """
        normalized_path = file_path.replace("\\", "/")
        for pattern in self.patterns:
            if pattern.match(normalized_path):
                return True
        return False
    
    @classmethod
    def from_file(cls, file_path: Path) -> "IgnorePattern":
        """
        Create IgnorePattern from a .ignore file.
        
        Args:
            file_path: Path to .ignore file
            
        Returns:
            IgnorePattern instance
        """
        if not file_path.exists():
            return cls([])
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            
            patterns = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
            
            return cls(patterns)
        except OSError as e:
            raise FileError(f"Failed to read ignore file {file_path}: {e}")
    
    @classmethod
    def empty(cls) -> "IgnorePattern":
        """Create an empty ignore pattern (no ignores)."""
        return cls([])


class ProjectFiles:
    """Handler for project files."""
    
    def __init__(self, project_dir: Path, ignore_pattern: Optional[IgnorePattern] = None):
        """
        Initialize with project directory.
        
        Args:
            project_dir: Root directory of the project
            ignore_pattern: Ignore pattern (loads from .ignore if not provided)
        """
        self.project_dir = project_dir
        self.ignore_pattern = ignore_pattern or IgnorePattern.from_file(
            project_dir / ".ignore"
        )
        self._file_cache: Optional[List[str]] = None
    
    def get_files(self) -> List[str]:
        """
        Get all project files (excluding ignored files).
        
        Returns:
            List of relative file paths
        """
        if self._file_cache is not None:
            return self._file_cache
        
        files = []
        for root, dirs, file_names in os.walk(self.project_dir):
            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file_name in file_names:
                if file_name.startswith('.'):
                    continue
                
                full_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(full_path, self.project_dir)
                relative_path = relative_path.replace("\\", "/")
                
                if not self.ignore_pattern.is_ignored(relative_path):
                    files.append(relative_path)
        
        self._file_cache = files
        return files
    
    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists in the project."""
        return (self.project_dir / file_path).exists()
    
    def get_full_path(self, file_path: str) -> Path:
        """Get full path for a relative file path."""
        return self.project_dir / file_path
    
    def clear_cache(self) -> None:
        """Clear the file cache."""
        self._file_cache = None


class ProjectConfig:
    """Handler for .config file."""
    
    def __init__(self, config_path: Path):
        """
        Initialize with config file path.
        
        Args:
            config_path: Path to .config file
        """
        self.config_path = config_path
        self._config: Optional[dict] = None
    
    def load(self) -> dict:
        """
        Load configuration from .config file.
        
        Returns:
            Dictionary of configuration values
        """
        if self._config is not None:
            return self._config
        
        if not self.config_path.exists():
            return {}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            config = {}
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        config[key] = value
            
            self._config = config
            return config
            
        except OSError as e:
            raise FileError(f"Failed to read config file {self.config_path}: {e}")
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a configuration value."""
        return self.load().get(key, default)
    
    def get_version(self) -> Optional[str]:
        """Get the version from configuration."""
        return self.get("version")
    
    def clear_cache(self) -> None:
        """Clear the configuration cache."""
        self._config = None