import pytest
from packages import parse, Version, InvalidVersion


class TestVersion:
    def test_parse_valid(self):
        v = parse("1.2.3")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.build == 0
        assert v.channel == "stable"
    
    def test_parse_with_channel(self):
        v = parse("1.2.3-beta.1")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.channel == "beta"
        assert v.channel_major == 1
    
    def test_parse_invalid(self):
        with pytest.raises(InvalidVersion):
            parse("invalid")
    
    def test_comparison(self):
        assert parse("1.0.0") < parse("2.0.0")
        assert parse("1.0.0-dev.1") < parse("1.0.0-beta.1")
        assert parse("1.0.0-beta.1") < parse("1.0.0")
    
    def test_promote(self):
        v = parse("1.0.0-dev.1")
        assert str(v.promote()) == "1.0.0-alpha.1"
        
        v = parse("1.0.0-alpha.1")
        assert str(v.promote()) == "1.0.0-beta.1"
        
        v = parse("1.0.0-rc.1")
        assert str(v.promote()) == "1.0.0"
    
    def test_next_patch(self):
        v = parse("1.2.3")
        assert str(v.next_patch()) == "1.2.4"
    
    def test_next_minor(self):
        v = parse("1.2.3")
        assert str(v.next_minor()) == "1.3.0"
    
    def test_next_major(self):
        v = parse("1.2.3")
        assert str(v.next_major()) == "2.0.0"