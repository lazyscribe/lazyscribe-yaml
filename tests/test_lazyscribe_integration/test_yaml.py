"""Test using the YAML handler with lazyscribe."""

import zoneinfo
from datetime import datetime

import time_machine
from lazyscribe import Project


@time_machine.travel(
    datetime(2025, 1, 20, 13, 23, 30, tzinfo=zoneinfo.ZoneInfo("UTC")), tick=False
)
def test_yaml_project_write(tmp_path):
    """Test logging an artifact using the YAML handler."""
    location = tmp_path / "my-project-location"
    location.mkdir()

    project = Project(fpath=location / "project.json", mode="w")
    with project.log("My experiment") as exp:
        exp.log_artifact(name="feature-names", value=["a", "b", "c"], handler="yaml")

    project.save()

    assert (
        location / "my-experiment-20250120132330" / "feature-names-20250120132330.yaml"
    ).is_file()

    project_r = Project(fpath=location / "project.json", mode="r")
    out = project_r["my-experiment"].load_artifact(name="feature-names")

    assert out == ["a", "b", "c"]
