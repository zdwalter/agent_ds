"""
Docker interaction skill using the Docker CLI.
"""

import json
import shlex
import subprocess
from typing import Any, Dict, List, Optional


def _run_docker_command(args: List[str], capture_output=True) -> Dict[str, Any]:
    """
    Run a docker command and return result.
    """
    cmd = ["docker"] + args
    try:
        result = subprocess.run(
            cmd, capture_output=capture_output, text=True, check=False
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip() if result.stdout else "",
            "stderr": result.stderr.strip() if result.stderr else "",
            "returncode": result.returncode,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Docker CLI not found. Ensure Docker is installed and in PATH.",
            "returncode": 127,
        }
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": str(e), "returncode": 1}


def docker_ps(all: bool = False) -> Dict[str, Any]:
    """
    List containers.
    """
    args = ["ps", "--format", "{{json .}}"]
    if all:
        args.append("-a")
    result = _run_docker_command(args)
    if result["success"] and result["stdout"]:
        lines = result["stdout"].strip().split("\n")
        containers = []
        for line in lines:
            if line:
                try:
                    containers.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        result["containers"] = containers
    return result


def docker_images() -> Dict[str, Any]:
    """
    List images.
    """
    args = ["images", "--format", "{{json .}}"]
    result = _run_docker_command(args)
    if result["success"] and result["stdout"]:
        lines = result["stdout"].strip().split("\n")
        images = []
        for line in lines:
            if line:
                try:
                    images.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        result["images"] = images
    return result


def docker_run(
    image: str,
    command: Optional[str] = None,
    ports: Optional[Dict[str, int]] = None,
    volumes: Optional[Dict[str, str]] = None,
    detach: bool = False,
    environment: Optional[Dict[str, str]] = None,
    name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run a container.
    """
    args = ["run"]
    if detach:
        args.append("-d")
    if ports:
        for host_port, container_port in ports.items():
            args.extend(["-p", f"{host_port}:{container_port}"])
    if volumes:
        for host_path, container_path in volumes.items():
            args.extend(["-v", f"{host_path}:{container_path}"])
    if environment:
        for key, value in environment.items():
            args.extend(["-e", f"{key}={value}"])
    if name:
        args.extend(["--name", name])
    args.append(image)
    if command:
        args.append(command)
    return _run_docker_command(args)


def docker_stop(container_id: str) -> Dict[str, Any]:
    """
    Stop a container.
    """
    args = ["stop", container_id]
    return _run_docker_command(args)


def docker_logs(container_id: str, tail: int = 10) -> Dict[str, Any]:
    """
    Fetch logs of a container.
    """
    args = ["logs", "--tail", str(tail), container_id]
    return _run_docker_command(args)
