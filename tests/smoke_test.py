"""Check that basic features work.

Used in our publishing pipeline.
"""

import tempfile
from pathlib import Path

from lazyscribe import Project

with tempfile.TemporaryDirectory() as tmpdir:
    # Create a project
    project = Project(Path(tmpdir) / "project.json", mode="w")
    with project.log(name="YAML experiment") as exp:
        exp.log_artifact(name="feature-names", value=["a", "b", "c"], handler="yaml")

    project.save()

    exp = project["yaml-experiment"]
    value = exp.load_artifact(name="feature-names")

    assert value == ["a", "b", "c"]
