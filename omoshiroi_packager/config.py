"""
Configuration management for the packages module.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from .exceptions import ConfigError


@dataclass
class Config:
    """
    Application configuration.
    
    Attributes:
        manifest_dir: Directory for manifest files
        project_dir: Root directory of the project
        tmp_dir: Temporary directory for build artifacts
    """
    
    manifest_dir: Path
    project_dir: Path
    tmp_dir: Path
    
    @classmethod
    def from_env(cls, load_dotenv_file: bool = True) -> Config:
        """
        Create configuration from environment variables.
        
        Args:
            load_dotenv_file: Whether to load .env file
            
        Returns:
            Config instance
            
        Raises:
            ConfigError: If required variables are missing
        """
        if load_dotenv_file:
            load_dotenv()
        
        manifest_dir = os.getenv("MANIFEST_DIR")
        project_dir = os.getenv("PROJECT_DIR")
        tmp_dir = os.getenv("TMP_DIR")
        
        missing = []
        if not manifest_dir:
            missing.append("MANIFEST_DIR")
        if not project_dir:
            missing.append("PROJECT_DIR")
        if not tmp_dir:
            missing.append("TMP_DIR")
        
        if missing:
            raise ConfigError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
        
        return cls(
            manifest_dir=Path(manifest_dir),
            project_dir=Path(project_dir),
            tmp_dir=Path(tmp_dir),
        )
    
    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        for dir_path in [self.manifest_dir, self.tmp_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @property
    def manifest_stable_path(self) -> Path:
        """Path to stable manifest file."""
        return self.manifest_dir / "manifest-stable.json"
    
    @property
    def manifest_beta_path(self) -> Path:
        """Path to beta manifest file."""
        return self.manifest_dir / "manifest-beta.json"
    
    def get_manifest_path(self, channel: str) -> Path:
        """
        Get manifest path for a channel.
        
        Args:
            channel: Channel name (stable, beta, dev, etc.)
            
        Returns:
            Path to manifest file
        """
        return self.manifest_dir / f"manifest-{channel}.json"
    
    def get_ignore_file_path(self) -> Path:
        """Get path to .ignore file."""
        return self.project_dir / ".ignore"
    
    def get_config_file_path(self) -> Path:
        """Get path to .config file."""
        return self.project_dir / ".config"