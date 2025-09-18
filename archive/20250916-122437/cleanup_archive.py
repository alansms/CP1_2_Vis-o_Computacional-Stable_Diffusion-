"""
Script de limpeza e arquivamento de artefatos gerados (frames, output, temp).

Uso:
  python cleanup_archive.py --archive
  python cleanup_archive.py --clean
  python cleanup_archive.py --archive --clean
"""

import os
import shutil
import time
from pathlib import Path


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def archive_outputs(base: Path):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    archive_dir = base / "archive" / timestamp
    ensure_dir(archive_dir)

    moved_any = False
    for name in ["frames", "output", "temp"]:
        src = base / name
        if src.exists() and any(src.iterdir()):
            dst = archive_dir / name
            ensure_dir(dst.parent)
            shutil.move(str(src), str(dst))
            moved_any = True
            # recriar diretório vazio
            ensure_dir(src)
    return archive_dir if moved_any else None


def clean_outputs(base: Path):
    removed = []
    for name in ["frames", "output", "temp"]:
        src = base / name
        if src.exists():
            shutil.rmtree(src)
            removed.append(str(src))
            ensure_dir(src)
    return removed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", action="store_true", help="Arquivar conteúdo atual em archive/<timestamp>")
    parser.add_argument("--clean", action="store_true", help="Limpar diretórios frames, output, temp")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent

    if args.archive:
        archived = archive_outputs(base)
        if archived:
            print(f"Arquivado em: {archived}")
        else:
            print("Nada para arquivar.")

    if args.clean:
        removed = clean_outputs(base)
        print(f"Diretórios limpos e recriados: {removed}")

    if not args.archive and not args.clean:
        parser.print_help()


