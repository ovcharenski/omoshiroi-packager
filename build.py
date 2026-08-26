#!/usr/bin/env python
"""
Build script for omoshiroi-packager.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd: list, description: str = None) -> None:
    """Run a command and check for errors."""
    if description:
        print(f"→ {description}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


def build() -> None:
    """Build the package."""
    print("Building omoshiroi-packager...\n")
    
    # Clean old builds
    for dir_name in ["build", "dist", "*.egg-info"]:
        if dir_name.startswith("*"):
            pattern = dir_name
            import glob
            for path in glob.glob(pattern):
                import shutil
                shutil.rmtree(path, ignore_errors=True)
        else:
            import shutil
            shutil.rmtree(dir_name, ignore_errors=True)
    
    # Install build dependencies
    run_command(
        [sys.executable, "-m", "pip", "install", "build", "twine"],
        "Installing build dependencies"
    )
    
    # Build
    run_command(
        [sys.executable, "-m", "build"],
        "Building package"
    )
    
    print("\n✅ Build complete!")
    print("📦 Run 'pip install -e .' to install in development mode")
    print("📦 Run 'twine upload dist/*' to upload to PyPI")


def test() -> None:
    """Run tests."""
    run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        "Running tests"
    )


def clean() -> None:
    """Clean build artifacts."""
    import shutil
    for pattern in ["build", "dist", "*.egg-info", ".pytest_cache", "__pycache__"]:
        if "*" in pattern:
            import glob
            for path in glob.glob(pattern):
                shutil.rmtree(path, ignore_errors=True)
        else:
            shutil.rmtree(pattern, ignore_errors=True)
    
    # Also clean __pycache__ in subdirectories
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            shutil.rmtree(os.path.join(root, "__pycache__"), ignore_errors=True)
    
    print("✅ Clean complete!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build and test omoshiroi-packager")
    parser.add_argument("command", nargs="?", default="build",
                       choices=["build", "test", "clean"],
                       help="Command to run")
    
    args = parser.parse_args()
    
    if args.command == "build":
        build()
    elif args.command == "test":
        test()
    elif args.command == "clean":
        clean()