#!/usr/bin/env python3

import argparse
import json
import subprocess
from pathlib import Path


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def metadata(root):
    return json.loads(
        subprocess.check_output(
            ["cargo", "metadata", "--locked", "--format-version", "1"], cwd=root
        )
    )


def dependencies(data):
    packages = {package["id"]: package for package in data["packages"]}
    nodes = {node["id"]: node for node in data["resolve"]["nodes"]}
    pending = [package["id"] for package in data["packages"] if package["source"] is None]
    seen = set()
    while pending:
        package = pending.pop()
        if package in seen:
            continue
        seen.add(package)
        pending.extend(dependency["pkg"] for dependency in nodes[package]["deps"])
    return [packages[package] for package in seen if packages[package]["source"] is not None]


def main():
    args = arguments()
    root = Path(__file__).resolve().parent.parent
    packages = {}
    for workspace in (root, root / "snolc-modules"):
        for package in dependencies(metadata(workspace)):
            packages[(package["name"], package["version"], package["source"])] = package

    output = ["snolc third-party notices", ""]
    for key in sorted(packages):
        package = packages[key]
        directory = Path(package["manifest_path"]).parent
        output.extend(
            [
                f"{package['name']} {package['version']}",
                f"license: {package.get('license') or 'see included license file'}",
                f"source: {package['source']}",
                "",
            ]
        )
        candidates = []
        if package.get("license_file"):
            candidates.append(directory / package["license_file"])
        for pattern in ("LICENSE*", "COPYING*", "NOTICE*"):
            candidates.extend(directory.glob(pattern))
        for path in sorted({path for path in candidates if path.is_file()}):
            output.extend([f"file: {path.name}", path.read_text(errors="replace").rstrip(), ""])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(output).rstrip() + "\n")


if __name__ == "__main__":
    main()
