import os
from pathlib import Path
from typing import Optional, Iterator

class TreeNode:
    def __init__(self, path: Path, is_last: bool = False, indent: str = ""):
        self.path = Path(path)
        self.is_last = is_last
        self.indent = indent

def list_directory(
    directory: str | Path = ".",
    max_depth: Optional[int] = None,
    show_hidden: bool = False
) -> Iterator[str]:
    """
    Generate a tree-like structure of directories and files.
    
    Args:
        directory: The starting directory path
        max_depth: Maximum depth to traverse (None for unlimited)
        show_hidden: Whether to show hidden files and directories
    
    Yields:
        Formatted strings representing the tree structure
    """
    directory = Path(directory)
    
    def should_include(path: Path) -> bool:
        return show_hidden or not path.name.startswith('.')
    
    def walk_directory(node: TreeNode, depth: int = 0) -> Iterator[str]:
        if max_depth is not None and depth > max_depth:
            return

        yield f"{node.indent}{'└── ' if node.is_last else '├── '}{node.path.name}"

        if node.path.is_dir():
            entries = [p for p in node.path.iterdir() if should_include(p)]
            entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
            
            for idx, entry in enumerate(entries):
                is_last = idx == len(entries) - 1
                new_indent = node.indent + ('    ' if node.is_last else '│   ')
                yield from walk_directory(
                    TreeNode(entry, is_last, new_indent),
                    depth + 1
                )

    yield directory.absolute().as_posix()
    entries = [p for p in directory.iterdir() if should_include(p)]
    entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
    
    for idx, entry in enumerate(entries):
        is_last = idx == len(entries) - 1
        yield from walk_directory(TreeNode(entry, is_last)) 