"""
Hashing utilities for the packages module.
"""

import hashlib
from pathlib import Path
from typing import Tuple

from ..exceptions import HashError


def generate_file_hash(file_path: Path, chunk_size: int = 4096) -> Tuple[str, str]:
    """
    Generate SHA256 and SHA512 hashes for a file.
    
    Args:
        file_path: Path to the file
        chunk_size: Size of chunks to read
        
    Returns:
        Tuple of (sha256_hash, sha512_hash)
        
    Raises:
        HashError: If file cannot be read
    """
    sha256_hash = hashlib.sha256()
    sha512_hash = hashlib.sha512()
    
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(byte_block)
                sha512_hash.update(byte_block)
    except OSError as e:
        raise HashError(f"Failed to hash file {file_path}: {e}")
    
    return sha256_hash.hexdigest(), sha512_hash.hexdigest()


def generate_string_hash(content: str) -> Tuple[str, str]:
    """
    Generate SHA256 and SHA512 hashes for a string.
    
    Args:
        content: String content
        
    Returns:
        Tuple of (sha256_hash, sha512_hash)
    """
    data = content.encode('utf-8')
    return (
        hashlib.sha256(data).hexdigest(),
        hashlib.sha512(data).hexdigest(),
    )


def verify_file_hash(file_path: Path, expected_sha256: str) -> bool:
    """
    Verify a file against an expected SHA256 hash.
    
    Args:
        file_path: Path to the file
        expected_sha256: Expected SHA256 hash
        
    Returns:
        True if hash matches
    """
    sha256, _ = generate_file_hash(file_path)
    return sha256 == expected_sha256