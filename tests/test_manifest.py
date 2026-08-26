import pytest
import json
from pathlib import Path
from packages import Config, ManifestManager, ProjectFiles


class TestManifest:
    def test_create_manifest(self, tmp_path):
        # Create test config
        config = Config(
            manifest_dir=tmp_path / "manifests",
            project_dir=tmp_path / "project",
            tmp_dir=tmp_path / "tmp",
        )
        
        # Create test project files
        project_dir = config.project_dir
        project_dir.mkdir(parents=True)
        (project_dir / "test.py").write_text("print('test')")
        
        # Create manifest
        manager = ManifestManager(config)
        manifest = manager.create_manifest("1.0.0", "stable")
        
        assert manifest.version == "1.0.0"
        assert manifest.channel == "stable"
        assert len(manifest.files) == 1
        assert manifest.files[0].path == "test.py"
    
    def test_save_load_manifest(self, tmp_path):
        config = Config(
            manifest_dir=tmp_path / "manifests",
            project_dir=tmp_path / "project",
            tmp_dir=tmp_path / "tmp",
        )
        
        manager = ManifestManager(config)
        
        # Create and save
        manifest = manager.create_manifest("1.0.0", "stable")
        manager.save_manifest(manifest, "stable")
        
        # Load
        loaded = manager.load_manifest("stable")
        assert loaded is not None
        assert loaded.version == "1.0.0"