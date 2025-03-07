import re
from sepicker._version import __version__


def test_version():
    pattern = r"^(\d+)\.(\d+)\.(\d+)$"
    assert re.match(pattern, __version__) is not None
