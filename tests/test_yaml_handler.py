"""Test the custom YAML artifact handler."""

import zoneinfo
from datetime import datetime

import pytest
import time_machine
import yaml

from lazyscribe_yaml import YAMLArtifact


@time_machine.travel(
    datetime(2025, 1, 20, 13, 23, 30, tzinfo=zoneinfo.ZoneInfo("UTC")), tick=False
)
@pytest.mark.parametrize(
    "data,Loader",
    (
        ([{"key": "value"}], yaml.SafeLoader),
        ([{"key": "value"}], yaml.FullLoader),
        ([{"type": float}], yaml.FullLoader),
        ({"key": "value", "type": str}, yaml.FullLoader),
    ),
)
def test_yaml_handler(data, Loader, tmp_path):
    """Test reading and writing YAML files with the handler."""
    location = tmp_path / "my-location"
    location.mkdir()
    handler = YAMLArtifact.construct(name="My output file")

    assert (
        handler.fname
        == f"my-output-file-{datetime.now().strftime('%Y%m%d%H%M%S')}.yaml"
    )

    with open(location / handler.fname, "w") as buf:
        handler.write(data, buf)

    assert (location / handler.fname).is_file()

    with open(location / handler.fname) as buf:
        out = handler.read(buf, Loader=Loader)

    assert data == out


@time_machine.travel(
    datetime(2025, 1, 20, 13, 23, 30, tzinfo=zoneinfo.ZoneInfo("UTC")), tick=False
)
def test_yaml_handler_defaults_to_safeloader(tmp_path):
    """Test YAML handler defaults to safe loader."""
    location = tmp_path / "my-location"
    location.mkdir()

    data = [{"key": "value"}]
    handler = YAMLArtifact.construct(name="My output file")

    assert (
        handler.fname
        == f"my-output-file-{datetime.now().strftime('%Y%m%d%H%M%S')}.yaml"
    )

    with open(location / handler.fname, "w") as buf:
        handler.write(data, buf)

    assert (location / handler.fname).is_file()

    with open(location / handler.fname) as buf:
        out = handler.read(buf)

    assert data == out

    # Test that it doesn't unserialize objects that need
    # full loader
    data = [{"type": float}]
    handler = YAMLArtifact.construct(name="Unreadable")

    assert handler.fname == f"unreadable-{datetime.now().strftime('%Y%m%d%H%M%S')}.yaml"

    with open(location / handler.fname, "w") as buf:
        handler.write(data, buf)

    assert (location / handler.fname).is_file()

    with (
        open(location / handler.fname) as buf,
        pytest.raises(yaml.constructor.ConstructorError),
    ):
        handler.read(buf)
