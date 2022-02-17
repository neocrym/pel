"""Utils for Docker and Docker Compose."""
import json
import shlex
import subprocess
from typing import Optional

from pel.datetime import str_datetime_to_unixtime


def docker_image_last_modified(
    *, image_name: str, docker_path: str = "docker"
) -> Optional[float]:
    """Return the Unix time of when a given Docker image was last modified."""
    quoted_docker_path = shlex.quote(docker_path)
    proc = subprocess.run(
        (quoted_docker_path, "inspect", image_name),
        text=True,
        capture_output=True,
        check=True,
    )
    if proc.returncode != 0:
        print(proc.stderr)
        return None
    metadata = json.loads(proc.stdout)
    return str_datetime_to_unixtime(metadata[0]["Created"])
