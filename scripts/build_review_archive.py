"""Create a complete, allowlisted source-review archive including plugin manifests."""
import argparse
from pathlib import Path
from prepare_harness import archive

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ("skills", "adapters", "scripts", "tests", "docs", ".claude-plugin", ".codex-plugin", ".github")
FILES = ("README.md", "INSTALL.md", "CONTRIBUTING.md", "ARCHITECTURE.md", "AGENTS.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "LICENSE.txt", "VERSION", "CHANGELOG.md", ".mcp.json", ".gitignore")


def build(root: Path, output: Path) -> None:
    if output.suffix != ".zip" or output.exists():
        raise ValueError("Choose a new review ZIP output path.")
    files = {}
    for name in FILES:
        if (root / name).is_file():
            files[name] = (root / name).read_bytes()
    for folder in FOLDERS:
        for path in sorted((root / folder).rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Refusing symlink in review source: {path}")
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            files[path.relative_to(root).as_posix()] = path.read_bytes()
    with output.open("xb") as destination:
        destination.write(archive(files))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(ROOT, args.output)
