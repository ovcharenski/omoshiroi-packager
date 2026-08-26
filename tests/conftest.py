from pathlib import Path

import pytest


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
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
def tmp_manifest_dir(tmp_path: Path) -> Path:
    """Create a temporary manifest directory."""
    manifest_dir = tmp_path / "manifests"
    manifest_dir.mkdir()
    return manifest_dir


@pytest.fixture
def test_config(tmp_project: Path, tmp_manifest_dir: Path, tmp_path: Path):
    """Create a test configuration."""
    from omoshiroi_packager import Config
    
    return Config(
        manifest_dir=tmp_manifest_dir,
        project_dir=tmp_project,
        tmp_dir=tmp_path / "tmp",
    )


@pytest.fixture
def sample_versions() -> list:
    """Provide a list of sample versions."""
    return [
        "1.0.0-dev.1",
        "1.0.0-alpha.1",
        "1.0.0-beta.1",
        "1.0.0-rc.1",
        "1.0.0",
        "1.0.0-hotfix.1",
        "1.1.0",
        "2.0.0",
    ]