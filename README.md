# Omoshiroi Packager

[![PyPI version](https://badge.fury.io/py/omoshiroi-packager.svg)](https://badge.fury.io/py/omoshiroi-packager)
[![Python](https://img.shields.io/pypi/pyversions/omoshiroi-packager.svg)](https://pypi.org/project/omoshiroi-packager/)
[![License](https://img.shields.io/pypi/l/omoshiroi-packager.svg)](https://github.com/ovcharenski/omoshiroi-packager/blob/main/LICENSE)

Version parser and packaging utilities with multiple channel support.

## Features

- ✅ **Version Parsing** - Parse versions with up to 4 digits
- ✅ **Multiple Channels** - Support for 6 channels: `dev`, `alpha`, `beta`, `rc`, `stable`, `hotfix`
- ✅ **Version Comparison** - Full comparison support (`<`, `>`, `==`, `<=`, `>=`, `!=`)
- ✅ **Channel Promotion/Demotion** - Move versions between channels
- ✅ **Version Manipulation** - Increment major, minor, patch, or build numbers
- ✅ **Manifest Generation** - Create and manage package manifests
- ✅ **File Hashing** - SHA256 and SHA512 hashing
- ✅ **ZIP Archive Creation** - Package files into ZIP archives
- ✅ **Update Checking** - Check for newer versions

## Installation

```bash
pip install omoshiroi-packager
```

## Quick Start

```python
from omoshiroi_packager import parse, Version

# Parse a version
v = parse("1.2.3-beta.1")
print(v)  # 1.2.3-beta.1

# Access components
print(v.major)          # 1
print(v.minor)          # 2
print(v.patch)          # 3
print(v.build)          # 0
print(v.channel)        # beta
print(v.channel_major)  # 1
```

## Version Format

```
X.X.x.x-[channel].X.x.x
```

Where:
- `X` - required digit
- `x` - optional digit

### Examples

```python
# Stable releases
parse("1.2.3")
parse("1.2.3.0")
parse("2.0.1.5")

# Pre-releases
parse("1.2.3-dev.1")
parse("1.2.3-alpha.1.0")
parse("1.2.3-beta.1")
parse("1.2.3-rc.1.0.5")

# Hotfix
parse("1.2.3-hotfix.1")
```

## Channels

Versions can belong to one of six channels (in order):

| Channel | Order | Description |
|---------|-------|-------------|
| `dev` | 0 | Development builds |
| `alpha` | 1 | Alpha releases |
| `beta` | 2 | Beta releases |
| `rc` | 3 | Release candidates |
| `stable` | 4 | Stable releases |
| `hotfix` | 5 | Hotfix releases |

## API Reference

### Version Class

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `major` | `int` | First digit of version |
| `minor` | `int` | Second digit of version |
| `patch` | `int` | Third digit of version (0 if not present) |
| `build` | `int` | Fourth digit of version (0 if not present) |
| `channel` | `str` | Channel name |
| `channel_order` | `int` | Channel order number |
| `channel_major` | `int` | First digit of channel version |
| `channel_minor` | `int` | Second digit of channel version |
| `channel_patch` | `int` | Third digit of channel version |
| `channel_version` | `Tuple[int, int, int]` | Channel version as tuple |
| `is_dev` | `bool` | Whether version is dev |
| `is_alpha` | `bool` | Whether version is alpha |
| `is_beta` | `bool` | Whether version is beta |
| `is_rc` | `bool` | Whether version is release candidate |
| `is_stable` | `bool` | Whether version is stable |
| `is_hotfix` | `bool` | Whether version is hotfix |
| `is_prerelease` | `bool` | Whether version is a pre-release (dev, alpha, beta, rc) |
| `is_release` | `bool` | Whether version is a release (stable, hotfix) |
| `base_version` | `str` | Version without channel suffix |
| `full_version` | `str` | Normalized 4-digit version |

#### Methods

| Method | Description | Example |
|--------|-------------|---------|
| `promote()` | Move to next channel | `dev.1` → `alpha.1` |
| `demote()` | Move to previous channel | `hotfix.1` → `stable` |
| `next_patch()` | Increment patch version | `1.2.3` → `1.2.4` |
| `next_minor()` | Increment minor version | `1.2.3` → `1.3.0` |
| `next_major()` | Increment major version | `1.2.3` → `2.0.0` |
| `with_build(build)` | Set build number | `1.2.3` → `1.2.3.5` |
| `with_channel(channel)` | Change channel | `1.2.3` → `1.2.3.0-beta.1` |
| `get_stable_version()` | Get stable version | `1.2.3-beta.1` → `1.2.3.0` |
| `to_dict()` | Convert to dictionary | Returns dict with all data |
| `to_tuple()` | Convert to tuple | Returns tuple representation |

### Functions

#### `parse(version: str) -> Version`

Parse a version string into a Version object.

```python
from omoshiroi_packager import parse

v = parse("1.2.3-beta.1")
```

#### `is_valid(version: str) -> bool`

Check if a version string is valid.

```python
from omoshiroi_packager import is_valid

print(is_valid("1.2.3"))        # True
print(is_valid("invalid"))      # False
```

#### `sort_versions(versions: List[str]) -> List[str]`

Sort version strings in ascending order.

```python
from omoshiroi_packager import sort_versions

versions = ["2.0.0", "1.0.0-beta.1", "1.0.0", "1.0.0-alpha.1"]
sorted_versions = sort_versions(versions)
# ['1.0.0-alpha.1', '1.0.0-beta.1', '1.0.0', '2.0.0']
```

#### `latest_version(versions: List[str]) -> Optional[str]`

Get the latest version from a list.

```python
from omoshiroi_packager import latest_version

versions = ["1.0.0", "1.0.0-beta.1", "2.0.0"]
latest = latest_version(versions)  # "2.0.0"
```

#### `latest_stable(versions: List[str]) -> Optional[str]`

Get the latest stable version from a list.

```python
from omoshiroi_packager import latest_stable

versions = ["1.0.0", "1.0.0-beta.1", "1.1.0"]
latest = latest_stable(versions)  # "1.1.0"
```

## Usage Examples

### Version Comparison

```python
from omoshiroi_packager import parse

v1 = parse("1.0.0-dev.1")
v2 = parse("1.0.0-alpha.1")
v3 = parse("1.0.0-beta.1")
v4 = parse("1.0.0-rc.1")
v5 = parse("1.0.0")
v6 = parse("1.0.0-hotfix.1")

print(v1 < v2)  # True (dev < alpha)
print(v2 < v3)  # True (alpha < beta)
print(v3 < v4)  # True (beta < rc)
print(v4 < v5)  # True (rc < stable)
print(v5 < v6)  # True (stable < hotfix)

print(v5 > v4)  # True (stable > rc)
print(v5 == parse("1.0.0"))  # True
```

### Channel Promotion and Demotion

```python
from omoshiroi_packager import parse

# Promote through channels
v = parse("1.0.0-dev.1")
print(v.promote())           # 1.0.0-alpha.1
print(v.promote().promote()) # 1.0.0-beta.1
print(v.promote().promote().promote().promote())  # 1.0.0

# Demote through channels
v = parse("1.0.0-hotfix.1")
print(v.demote())            # 1.0.0
print(v.demote().demote())   # 1.0.0-rc.1
```

### Version Increment

```python
from omoshiroi_packager import parse

v = parse("1.2.3")
print(v.next_patch())   # 1.2.4
print(v.next_minor())   # 1.3.0
print(v.next_major())   # 2.0.0

# With channel
v = parse("1.2.3-beta.1")
print(v.next_patch())   # 1.2.4
```

### Working with Build Numbers

```python
from omoshiroi_packager import parse

v = parse("1.2.3")
print(v.with_build(5))          # 1.2.3.5

v = parse("1.2.3-beta.1")
print(v.with_build(10))         # 1.2.3.10-beta.1
```

### Changing Channels

```python
from omoshiroi_packager import parse

v = parse("1.2.3")
print(v.with_channel("beta"))   # 1.2.3.0-beta.1
print(v.with_channel("stable")) # 1.2.3.0
```

### Getting Stable Versions

```python
from omoshiroi_packager import parse

v = parse("1.2.3-beta.1")
print(v.get_stable_version())   # 1.2.3.0

v = parse("1.2.3")
print(v.get_stable_version())   # 1.2.3.0
```

### Serialization

```python
from omoshiroi_packager import parse, Version

v = parse("1.2.3-beta.1.0.5")

# Convert to dictionary
d = v.to_dict()
print(d)
# {
#     "major": 1,
#     "minor": 2,
#     "patch": 3,
#     "build": 0,
#     "channel": "beta",
#     "channel_version": {"major": 1, "minor": 0, "patch": 5},
#     ...
# }

# Convert to tuple
t = v.to_tuple()
# (1, 2, 3, 0, "beta", 1, 0, 5)

# Create from tuple
v2 = Version.from_tuple(t)
print(v2)  # 1.2.3-beta.1.0.5
```

## Configuration

Create a `.env` file with:

```env
MANIFEST_DIR=/path/to/manifests
PROJECT_DIR=/path/to/project
TMP_DIR=/path/to/tmp
```

```python
from omoshiroi_packager import Config, get_config

# Load from environment
config = Config.from_env()
config.ensure_directories()

# Or use global config
config = get_config()
```

## Manifest Management

```python
from omoshiroi_packager import Config, ManifestManager

config = Config(
    manifest_dir="/path/to/manifests",
    project_dir="/path/to/project",
    tmp_dir="/path/to/tmp",
)

manager = ManifestManager(config)

# Create a manifest
manifest = manager.create_manifest("1.0.0", "stable")

# Save to disk
manager.save_manifest(manifest, "stable")

# Load from disk
loaded = manager.load_manifest("stable")
print(loaded.version)  # "1.0.0"

# Get version from manifest
version = manager.get_version("stable")  # "1.0.0"

# Get all manifests
all_manifests = manager.get_all_manifests()
```

## Update Checking

```python
from omoshiroi_packager import get_latest_version, check_update

# Get latest version for a channel
latest = get_latest_version("stable")
print(f"Latest stable: {latest}")

# Check for updates
result = check_update("1.0.0", channel="stable")
if result["update_required"]:
    print(f"Update available! Latest: {result['latest_version']}")
else:
    print("Up to date!")
```

## Packaging

```python
from omoshiroi_packager import pack_version, make_manifest

# Create a manifest
manifest_path = make_manifest("1.0.0", "stable")

# Package a version
zip_data, manifest_path = pack_version("1.0.0", "stable")

# Or package by channel
zip_data, manifest_path = pack_by_channel("stable")

# Save the ZIP file
with open("package.zip", "wb") as f:
    f.write(zip_data.getvalue())
```

## File Utilities

```python
from omoshiroi_packager import generate_file_hash, verify_file_hash
from pathlib import Path

# Generate file hashes
sha256, sha512 = generate_file_hash(Path("file.txt"))

# Verify file hash
is_valid = verify_file_hash(Path("file.txt"), expected_sha256)
```

## ZIP Utilities

```python
from omoshiroi_packager import create_zip_from_files, extract_zip
from pathlib import Path

# Create ZIP from files
files = ["file1.txt", "file2.txt"]
zip_data = create_zip_from_files(
    files=files,
    base_dir=Path("/path/to/base"),
    manifest_path=Path("/path/to/manifest.json"),
)

# Extract ZIP
extract_zip(zip_data, Path("/path/to/extract"))

# Get list of files in ZIP
file_list = get_zip_file_list(zip_data)
```

## Development

```bash
# Clone repository
git clone https://github.com/ovcharenski/omoshiroi-packager.git
cd omoshiroi-packager

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Build package
python -m build

# Format code
black .
ruff check --fix .

# Run linters
ruff check .
mypy .
```

## License

MIT

## Author

ovcharenski

## Links

- [Homepage](https://ns-staff.ovcharenski.ru/projects/omoshiroi-packager)
- [Repository](https://github.com/ovcharenski/omoshiroi-packager)
- [PyPI](https://pypi.org/project/omoshiroi-packager/)