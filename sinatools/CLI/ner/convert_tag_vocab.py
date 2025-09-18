"""CLI helper to convert legacy torchtext tag vocabularies."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from sinatools.ner.tag_vocab import convert_tag_vocab_file


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a legacy tag_vocab.pkl to the native SinaTools format",
    )
    parser.add_argument(
        "model_dir",
        type=Path,
        help="Directory that contains tag_vocab.pkl (e.g. models/sinatools/Wj27012000.tar)",
    )
    parser.add_argument(
        "--backup-suffix",
        default=".legacy",
        help="Suffix used for the backup copy (default: .legacy)",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating a backup copy before rewriting tag_vocab.pkl",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report whether conversion is needed without writing files",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    model_dir: Path = args.model_dir
    pickle_path = model_dir / "tag_vocab.pkl"

    if not pickle_path.exists():
        parser.error(f"No tag_vocab.pkl found at {pickle_path}")

    backup_suffix = None if args.no_backup else args.backup_suffix

    try:
        converted, backup_path = convert_tag_vocab_file(
            model_dir,
            backup_suffix=backup_suffix,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # pragma: no cover - CLI surface
        parser.error(str(exc))

    if args.dry_run:
        if converted:
            parser.exit(0, "Conversion required (dry-run).\n")
        parser.exit(0, "No conversion required.\n")

    if not converted:
        parser.exit(0, "tag_vocab.pkl already uses the native format.\n")

    message = "Converted tag_vocab.pkl" if backup_suffix is None else (
        f"Converted tag_vocab.pkl (backup saved to {backup_path})"
    )
    parser.exit(0, message + "\n")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
