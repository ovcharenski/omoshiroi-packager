import pytest
from pathlib import Path


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project structure."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    
    # Create some files
    (project_dir / "main.py").write_text("print('main')")
    (project_dir / "utils.py").write_text("print('utils')")
    
    # Create subdirectory with file
    subdir = project_dir / "sub"
    subdir.mkdir()
    (subdir / "module.py").write_text("print('module')")
    
    return project_dir


@pytest.fixture
def tmp_manifest_dir(tmp_path):
    """Create a temporary manifest directory."""
    manifest_dir = tmp_path / "manifests"
    manifest_dir.mkdir()
    return manifest_dir


@pytest.fixture
def test_config(tmp_project, tmp_manifest_dir, tmp_path):
    """Create a test configuration."""
    from packages import Config
    return Config(
        manifest_dir=tmp_manifest_dir,
        project_dir=tmp_project,
        tmp_dir=tmp_path / "tmp",
    )