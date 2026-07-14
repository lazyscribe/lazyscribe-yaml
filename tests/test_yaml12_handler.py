"""Test the YAML12 artifact handler."""

import zoneinfo
from datetime import datetime

import pytest
import time_machine
import yaml12

from lazyscribe_yaml import YAML12Artifact


@time_machine.travel(
    datetime(2025, 1, 20, 13, 23, 30, tzinfo=zoneinfo.ZoneInfo("UTC")), tick=False
)
@pytest.mark.parametrize(
    "data",
    (
        [{"key": "value"}],
        {"key": "value", "number": 42},
        ["a", "b", "c"],
    ),
)
def test_yaml12_handler(data, tmp_path):
    """Test reading and writing YAML files with the handler."""
    location = tmp_path / "my-location"
    location.mkdir()
    handler = YAML12Artifact.construct(name="My output file")

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


@time_machine.travel(
    datetime(2025, 1, 20, 13, 23, 30, tzinfo=zoneinfo.ZoneInfo("UTC")), tick=False
)
def test_yaml12_booleans(tmp_path):
    """Test YAML 1.2 boolean semantics differ from YAML 1.1.

    In YAML 1.2, only true/false are booleans. yes/no are plain strings.
    """
    location = tmp_path / "my-location"
    location.mkdir()
    handler = YAML12Artifact.construct(name="booleans")

    # True/False round-trips correctly
    data = {"enabled": True, "disabled": False}
    with open(location / handler.fname, "w") as buf:
        handler.write(data, buf)
    with open(location / handler.fname) as buf:
        out = handler.read(buf)
    assert out == {"enabled": True, "disabled": False}

    # yes/no are strings in YAML 1.2, not booleans
    yaml_text = "enabled: yes\ndisabled: no\n"
    other_fname = location / "yes-no.yaml"
    other_fname.write_text(yaml_text)
    with open(other_fname) as buf:
        out = handler.read(buf)
    assert out == {"enabled": "yes", "disabled": "no"}


@time_machine.travel(
    datetime(2025, 1, 20, 13, 23, 30, tzinfo=zoneinfo.ZoneInfo("UTC")), tick=False
)
def test_yaml12_handler_multi(tmp_path):
    """Test multi-document streams via multi=True kwarg."""
    location = tmp_path / "my-location"
    location.mkdir()
    handler = YAML12Artifact.construct(name="multi-doc")

    docs = [{"a": 1}, {"b": 2}]
    with open(location / handler.fname, "w") as buf:
        handler.write(docs, buf, multi=True)

    with open(location / handler.fname) as buf:
        out = handler.read(buf, multi=True)

    assert out == docs


@time_machine.travel(
    datetime(2025, 1, 20, 13, 23, 30, tzinfo=zoneinfo.ZoneInfo("UTC")), tick=False
)
def test_yaml12_handler_anchors(tmp_path):
    """Test that YAML anchors/aliases are resolved correctly on read."""
    location = tmp_path / "my-location"
    location.mkdir()
    handler = YAML12Artifact.construct(name="anchors")

    yaml_text = "shared: &ref\n  x: 1\n  y: 2\ncopy: *ref\n"
    fpath = location / handler.fname
    fpath.write_text(yaml_text)

    with open(fpath) as buf:
        out = handler.read(buf)

    assert out == {"shared": {"x": 1, "y": 2}, "copy": {"x": 1, "y": 2}}


@time_machine.travel(
    datetime(2025, 1, 20, 13, 23, 30, tzinfo=zoneinfo.ZoneInfo("UTC")), tick=False
)
def test_yaml12_handler_tagged_nodes_wrapped(tmp_path):
    """Test that tagged nodes without a handler are wrapped in yaml12.Yaml."""
    location = tmp_path / "my-location"
    location.mkdir()
    handler = YAML12Artifact.construct(name="tagged")

    yaml_text = "value: !mytag foo\n"
    fpath = location / handler.fname
    fpath.write_text(yaml_text)

    with open(fpath) as buf:
        out = handler.read(buf)

    assert isinstance(out["value"], yaml12.Yaml)
    assert out["value"].tag == "!mytag"
    assert out["value"].value == "foo"


@time_machine.travel(
    datetime(2025, 1, 20, 13, 23, 30, tzinfo=zoneinfo.ZoneInfo("UTC")), tick=False
)
def test_yaml12_handler_tag_handlers(tmp_path):
    """Test that custom tag handlers are applied via the handlers kwarg."""
    location = tmp_path / "my-location"
    location.mkdir()
    handler = YAML12Artifact.construct(name="tag-handlers")

    yaml_text = "value: !upper hello\n"
    fpath = location / handler.fname
    fpath.write_text(yaml_text)

    with open(fpath) as buf:
        out = handler.read(buf, handlers={"!upper": str.upper})

    assert out == {"value": "HELLO"}
