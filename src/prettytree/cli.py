import argparse
import sys
from pathlib import Path
from .core import list_directory

def main():
    parser = argparse.ArgumentParser(
        description="Display directory structure in a tree-like format"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to list (default: current directory)",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        help="Maximum depth to traverse",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Show hidden files and directories",
    )

    args = parser.parse_args()

    try:
        for line in list_directory(
            args.directory,
            max_depth=args.max_depth,
            show_hidden=args.all
        ):
            print(line)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 