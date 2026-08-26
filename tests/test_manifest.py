import pytest
from pathlib import Path

from omoshiroi_packager import Config, ManifestManager


class TestManifest:
    def test_create_manifest(self, tmp_path: Path):
        """Test creating a manifest."""
        config = Config(
            manifest_dir=tmp_path / "manifests",
            project_dir=tmp_path / "project",
            tmp_dir=tmp_path / "tmp",
        )
        
        project_dir = config.project_dir
        project_dir.mkdir(parents=True)
        (project_dir / "test.py").write_text("print('test')")
        (project_dir / "test2.py").write_text("print('test2')")
        
        manager = ManifestManager(config)
        manifest = manager.create_manifest("1.0.0", "stable")
        
        assert manifest.version == "1.0.0"
        assert manifest.channel == "stable"
        assert len(manifest.files) > 0
        assert any(f.path == "test.py" for f in manifest.files)
    
    def test_save_load_manifest(self, tmp_path: Path):
        """Test saving and loading a manifest."""
        config = Config(
            manifest_dir=tmp_path / "manifests",
            project_dir=tmp_path / "project",
            tmp_dir=tmp_path / "tmp",
        )
        
        project_dir = config.project_dir
        project_dir.mkdir(parents=True)
        (project_dir / "test.py").write_text("print('test')")
        
        manager = ManifestManager(config)
        
        manifest = manager.create_manifest("1.0.0", "stable")
        manager.save_manifest(manifest, "stable")
        
        loaded = manager.load_manifest("stable")
        assert loaded is not None
        assert loaded.version == "1.0.0"
        assert len(loaded.files) == 1
    
    def test_load_nonexistent(self, tmp_path: Path):
        """Test loading a non-existent manifest."""
        config = Config(
            manifest_dir=tmp_path / "manifests",
            project_dir=tmp_path / "project",
            tmp_dir=tmp_path / "tmp",
        )
        
        manager = ManifestManager(config)
        manifest = manager.load_manifest("nonexistent")
        assert manifest is None
    
    def test_get_version(self, tmp_path: Path):
        """Test getting version from manifest."""
        config = Config(
            manifest_dir=tmp_path / "manifests",
            project_dir=tmp_path / "project",
            tmp_dir=tmp_path / "tmp",
        )
        
        project_dir = config.project_dir
        project_dir.mkdir(parents=True)
        (project_dir / "test.py").write_text("print('test')")
        
        manager = ManifestManager(config)
        
        version = manager.get_version("stable")
        assert version is None
        
        manifest = manager.create_manifest("1.2.3", "stable")
        manager.save_manifest(manifest, "stable")
        
        version = manager.get_version("stable")
        assert version == "1.2.3"
    
    def test_get_all_manifests(self, tmp_path: Path):
        """Test getting all manifests."""
        config = Config(
            manifest_dir=tmp_path / "manifests",
            project_dir=tmp_path / "project",
            tmp_dir=tmp_path / "tmp",
        )
        
        project_dir = config.project_dir
        project_dir.mkdir(parents=True)
        (project_dir / "test.py").write_text("print('test')")
        
        manager = ManifestManager(config)
        
        channels = ["dev", "beta", "stable"]
        for channel in channels:
            manifest = manager.create_manifest(f"1.0.0-{channel}.1", channel)
            manager.save_manifest(manifest, channel)
        
        all_manifests = manager.get_all_manifests()
        
        for channel in channels:
            assert channel in all_manifests
            assert all_manifests[channel] is not None