import pytest

from omoshiroi_packager import InvalidVersion, Version, parse, sort_versions, latest_version, latest_stable


class TestVersion:
    def test_parse_valid(self):
        """Test parsing valid version strings."""
        v = parse("1.2.3")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.build == 0
        assert v.channel == "stable"
    
    def test_parse_two_digits(self):
        """Test parsing version with 2 digits."""
        v = parse("1.2")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 0
        assert v.build == 0
        assert v.channel == "stable"
    
    def test_parse_four_digits(self):
        """Test parsing version with 4 digits."""
        v = parse("1.2.3.4")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.build == 4
        assert v.channel == "stable"
    
    def test_parse_with_channel(self):
        """Test parsing version with channel."""
        v = parse("1.2.3-beta.1")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.build == 0
        assert v.channel == "beta"
        assert v.channel_major == 1
    
    def test_parse_with_channel_full(self):
        """Test parsing version with full channel version."""
        v = parse("1.2.3.0-beta.1.0.5")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.build == 0
        assert v.channel == "beta"
        assert v.channel_major == 1
        assert v.channel_minor == 0
        assert v.channel_patch == 5
    
    def test_parse_all_channels(self):
        """Test parsing all channel types."""
        channels = ["dev", "alpha", "beta", "rc", "stable", "hotfix"]
        for channel in channels:
            if channel == "stable":
                v = parse("1.0.0")
                assert v.channel == "stable"
            else:
                v = parse(f"1.0.0-{channel}.1")
                assert v.channel == channel
    
    def test_parse_invalid(self):
        """Test parsing invalid version strings."""
        invalid_versions = [
            "invalid",
            "1",
            "1.2.3-beta",
            "1.2.3-",
            "1.2.3-beta.",
            "1.2.3-xyz.1",
        ]
        for version in invalid_versions:
            with pytest.raises(InvalidVersion):
                parse(version)
    
    def test_comparison(self):
        """Test version comparison."""
        assert parse("1.0.0") < parse("2.0.0")
        assert parse("1.0.0-dev.1") < parse("1.0.0-alpha.1")
        assert parse("1.0.0-alpha.1") < parse("1.0.0-beta.1")
        assert parse("1.0.0-beta.1") < parse("1.0.0-rc.1")
        assert parse("1.0.0-rc.1") < parse("1.0.0")
        assert parse("1.0.0") < parse("1.0.0-hotfix.1")
    
    def test_comparison_same_channel(self):
        """Test comparison within same channel."""
        assert parse("1.0.0-dev.1") < parse("1.0.0-dev.2")
        assert parse("1.0.0-dev.1.0") < parse("1.0.0-dev.1.1")
        assert parse("1.0.0-beta.1") < parse("1.0.0-beta.2")
    
    def test_promote(self):
        """Test version promotion."""
        v = parse("1.0.0-dev.1")
        # __str__ hides trailing .0, so "1.0-alpha.1" instead of "1.0.0-alpha.1"
        assert str(v.promote()) == "1.0-alpha.1"
        
        v = parse("1.0.0-alpha.1")
        assert str(v.promote()) == "1.0-beta.1"
        
        v = parse("1.0.0-beta.1")
        assert str(v.promote()) == "1.0-rc.1"
        
        v = parse("1.0.0-rc.1")
        assert str(v.promote()) == "1.0"
        
        v = parse("1.0.0")
        assert str(v.promote()) == "1.0"
    
    def test_demote(self):
        """Test version demotion."""
        v = parse("1.0.0-hotfix.1")
        # __str__ hides trailing .0
        assert str(v.demote()) == "1.0"
        
        v = parse("1.0.0")
        assert str(v.demote()) == "1.0-rc.1"
        
        v = parse("1.0.0-rc.1")
        assert str(v.demote()) == "1.0-beta.1"
        
        v = parse("1.0.0-dev.1")
        assert str(v.demote()) == "1.0-dev.1"
    
    def test_next_patch(self):
        """Test patch increment."""
        v = parse("1.2.3")
        assert str(v.next_patch()) == "1.2.4"
        
        v = parse("1.2.3-beta.1")
        assert str(v.next_patch()) == "1.2.4"
    
    def test_next_minor(self):
        """Test minor increment."""
        v = parse("1.2.3")
        # __str__ hides trailing .0
        assert str(v.next_minor()) == "1.3"
        
        v = parse("1.2.3-beta.1")
        assert str(v.next_minor()) == "1.3"
    
    def test_next_major(self):
        """Test major increment."""
        v = parse("1.2.3")
        # __str__ hides trailing .0
        assert str(v.next_major()) == "2.0"
        
        v = parse("1.2.3-beta.1")
        assert str(v.next_major()) == "2.0"
    
    def test_with_build(self):
        """Test setting build number."""
        v = parse("1.2.3")
        assert str(v.with_build(5)) == "1.2.3.5"
        
        v = parse("1.2.3-beta.1")
        assert str(v.with_build(5)) == "1.2.3.5-beta.1"
    
    def test_with_channel(self):
        """Test changing channel."""
        v = parse("1.2.3")
        # __str__ hides trailing .0
        assert str(v.with_channel("beta")) == "1.2.3-beta.1"
        assert str(v.with_channel("stable")) == "1.2.3"
        
        v = parse("1.2.3-beta.1")
        assert str(v.with_channel("alpha")) == "1.2.3-alpha.1"
    
    def test_get_stable_version(self):
        """Test getting stable version."""
        v = parse("1.2.3-beta.1")
        # __str__ hides trailing .0
        assert str(v.get_stable_version()) == "1.2.3"
        
        v = parse("1.2.3")
        assert str(v.get_stable_version()) == "1.2.3"
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        v = parse("1.2.3-beta.1.0.5")
        d = v.to_dict()
        
        assert d["major"] == 1
        assert d["minor"] == 2
        assert d["patch"] == 3
        assert d["build"] == 0
        assert d["channel"] == "beta"
        assert d["is_prerelease"] is True
        assert d["base_version"] == "1.2.3"
        assert d["channel_version"]["major"] == 1
        assert d["channel_version"]["minor"] == 0
        assert d["channel_version"]["patch"] == 5
    
    def test_to_tuple(self):
        """Test conversion to tuple."""
        v = parse("1.2.3-beta.1.0.5")
        t = v.to_tuple()
        
        assert t == (1, 2, 3, 0, "beta", 1, 0, 5)
    
    def test_from_tuple(self):
        """Test creation from tuple."""
        t = (1, 2, 3, 0, "beta", 1, 0, 5)
        v = Version.from_tuple(t)
        # __str__ hides trailing .0 in channel version
        assert str(v) == "1.2.3-beta.1.5"
    
    def test_sort_versions(self):
        """Test sorting versions."""
        versions = [
            "2.0.0",
            "1.0.0-beta.1",
            "1.0.0-dev.1",
            "1.0.0",
            "1.0.0-alpha.1",
        ]
        sorted_versions = sort_versions(versions)
        expected = [
            "1.0.0-dev.1",
            "1.0.0-alpha.1",
            "1.0.0-beta.1",
            "1.0.0",
            "2.0.0",
        ]
        assert sorted_versions == expected
    
    def test_latest_version(self):
        """Test getting latest version."""
        versions = [
            "1.0.0",
            "1.0.0-beta.1",
            "2.0.0",
            "1.0.0-alpha.1",
        ]
        assert latest_version(versions) == "2.0.0"
        assert latest_version([]) is None
    
    def test_latest_stable(self):
        """Test getting latest stable version."""
        versions = [
            "1.0.0",
            "1.0.0-beta.1",
            "2.0.0",
            "1.0.0-alpha.1",
            "1.1.0",
        ]
        assert latest_stable(versions) == "2.0.0"
        assert latest_stable([]) is None
        
        versions = ["1.0.0-beta.1", "1.0.0-alpha.1"]
        assert latest_stable(versions) is None
    
    def test_is_prerelease(self):
        """Test prerelease detection."""
        assert parse("1.0.0-dev.1").is_prerelease is True
        assert parse("1.0.0-alpha.1").is_prerelease is True
        assert parse("1.0.0-beta.1").is_prerelease is True
        assert parse("1.0.0-rc.1").is_prerelease is True
        assert parse("1.0.0").is_prerelease is False
        assert parse("1.0.0-hotfix.1").is_prerelease is False
    
    def test_channel_properties(self):
        """Test channel property methods."""
        v = parse("1.0.0-dev.1")
        assert v.is_dev is True
        assert v.is_alpha is False
        assert v.is_beta is False
        assert v.is_rc is False
        assert v.is_stable is False
        assert v.is_hotfix is False
        
        v = parse("1.0.0-beta.1")
        assert v.is_dev is False
        assert v.is_alpha is False
        assert v.is_beta is True
        assert v.is_rc is False
        assert v.is_stable is False
        assert v.is_hotfix is False
        
        v = parse("1.0.0")
        assert v.is_dev is False
        assert v.is_alpha is False
        assert v.is_beta is False
        assert v.is_rc is False
        assert v.is_stable is True
        assert v.is_hotfix is False