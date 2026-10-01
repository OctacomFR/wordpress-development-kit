"""Produce comparison evidence with ImageMagick, without deciding visual fidelity."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], *, allow_difference: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    allowed = {0, 1} if allow_difference else {0}
    if result.returncode not in allowed:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"ImageMagick a échoué ({result.returncode}) : {detail}")
    return result


def inspect_png(magick: str, path: Path) -> tuple[int, int]:
    if not path.is_file() or path.suffix.lower() != ".png":
        raise ValueError(f"Capture PNG absente ou format non pris en charge : {path}")
    result = run([magick, "identify", "-format", "%m %w %h\n", str(path)])
    match = re.fullmatch(r"PNG ([1-9][0-9]*) ([1-9][0-9]*)\s*", result.stdout)
    if not match:
        raise ValueError(f"Une seule image PNG est requise : {path}")
    return int(match[1]), int(match[2])


def compare_visuals(figma: Path, front: Path, output_dir: Path, *, magick: str = "magick") -> dict:
    executable = shutil.which(magick)
    if executable is None:
        raise ValueError("ImageMagick est requis : commande magick introuvable")
    figma = figma.resolve()
    front = front.resolve()
    output_dir = output_dir.resolve()
    if output_dir.exists():
        raise ValueError("Le dossier de sortie doit être nouveau pour conserver les preuves précédentes")
    if figma == front:
        raise ValueError("Deux captures distinctes Figma et front sont requises")

    figma_size = inspect_png(executable, figma)
    front_size = inspect_png(executable, front)
    if figma_size != front_size:
        raise ValueError(
            f"Dimensions différentes : Figma {figma_size}, front {front_size}. "
            "Examiner la cause sans redimensionner ni tronquer les captures."
        )
    version = run([executable, "-version"]).stdout.splitlines()[0]
    hashes = {"figma": sha256(figma), "front": sha256(front)}
    output_dir.mkdir(parents=True, exist_ok=False)
    outputs = {
        "side_by_side": output_dir / "side-by-side.png",
        "overlay": output_dir / "overlay.png",
        "difference": output_dir / "difference.png",
    }
    commands = [
        [executable, str(figma), str(front), "+append", str(outputs["side_by_side"])],
        [
            executable, str(figma), str(front), "-compose", "blend",
            "-define", "compose:args=50,50", "-composite", str(outputs["overlay"]),
        ],
        [
            executable, "compare", "-metric", "RMSE",
            str(figma), str(front), str(outputs["difference"]),
        ],
    ]
    run(commands[0])
    run(commands[1])
    metric = run(commands[2], allow_difference=True)
    match = re.fullmatch(
        r"([0-9.eE+\-]+)\s+\(([0-9.eE+\-]+)\)\s*", metric.stderr
    )
    if not match:
        raise ValueError(f"Mesure RMSE ImageMagick illisible : {metric.stderr.strip()}")
    width, height = figma_size
    expected_sizes = {
        "side_by_side": (width * 2, height),
        "overlay": figma_size,
        "difference": figma_size,
    }
    for name, path in outputs.items():
        if inspect_png(executable, path) != expected_sizes[name]:
            raise ValueError(f"Dimensions de sortie inattendues : {path}")
    if sha256(figma) != hashes["figma"] or sha256(front) != hashes["front"]:
        raise ValueError("Une capture source a changé pendant la comparaison ; refaire les preuves")

    evidence = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "tool": version,
        "inputs": {
            name: {"path": str(path), "sha256": hashes[name], "width": width, "height": height}
            for name, path in (("figma", figma), ("front", front))
        },
        "outputs": {
            name: {"path": str(path), "sha256": sha256(path)}
            for name, path in outputs.items()
        },
        "rmse": {"absolute": float(match[1]), "normalized": float(match[2])},
        "commands": commands,
        "visual_review_required": True,
    }
    (output_dir / "comparison.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figma", required=True, type=Path)
    parser.add_argument("--front", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        compare_visuals(args.figma, args.front, args.output_dir)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Supports produits : {args.output_dir.resolve()}")
    print("Examen visuel obligatoire ; aucune décision automatique de conformité.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
