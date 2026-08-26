"""
ZIP utilities for the packages module.
"""

from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path
from typing import List, Optional

from ..exceptions import PackError


def create_zip_from_files(
    files: List[str],
    base_dir: Path,
    manifest_path: Optional[Path] = None,
    compression: int = zipfile.ZIP_DEFLATED,
) -> BytesIO:
    """
    Create a ZIP archive from a list of files.

    Args:
        files: List of relative file paths
        base_dir: Base directory for resolving file paths
        manifest_path: Optional manifest file to include
        compression: ZIP compression method

    Returns:
        BytesIO object containing the ZIP archive

    Raises:
        PackError: If files cannot be added to the archive
    """
    memory_file = BytesIO()

    try:
        with zipfile.ZipFile(memory_file, "w", compression) as zipf:
            for file_path in files:
                full_path = base_dir / file_path

                if not full_path.exists():
                    print(f"Warning: File {full_path} does not exist")
                    continue

                # Use relative path as arcname
                arcname = file_path.replace("\\", "/")
                zipf.write(full_path, arcname)

            # Include manifest if provided
            if manifest_path and manifest_path.exists():
                arcname = manifest_path.name
                zipf.write(manifest_path, arcname)

    except OSError as e:
        raise PackError(f"Failed to create ZIP archive: {e}")

    memory_file.seek(0)
    return memory_file


def extract_zip(zip_data: BytesIO, extract_dir: Path) -> None:
    """
    Extract a ZIP archive to a directory.

    Args:
        zip_data: BytesIO object containing ZIP data
        extract_dir: Directory to extract to

    Raises:
        PackError: If extraction fails
    """
    try:
        extract_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_data, "r") as zipf:
            zipf.extractall(extract_dir)
    except OSError as e:
        raise PackError(f"Failed to extract ZIP archive: {e}")
    except zipfile.BadZipFile as e:
        raise PackError(f"Invalid ZIP archive: {e}")


def get_zip_file_list(zip_data: BytesIO) -> List[str]:
    """
    Get list of files in a ZIP archive.

    Args:
        zip_data: BytesIO object containing ZIP data

    Returns:
        List of file names in the archive
    """
    try:
        with zipfile.ZipFile(zip_data, "r") as zipf:
            return [info.filename for info in zipf.infolist() if not info.is_dir()]
    except zipfile.BadZipFile as e:
        raise PackError(f"Invalid ZIP archive: {e}")
