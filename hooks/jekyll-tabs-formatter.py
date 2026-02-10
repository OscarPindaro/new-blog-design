#!/usr/bin/env python3
"""Add tabs: true to Jekyll posts that use {% tabs %} liquid tags."""

import sys
import re
from pathlib import Path
from typing import List

import typer


app = typer.Typer(add_completion=False)


def has_tabs_tag(content: str) -> bool:
    """Check if content contains {% tabs %} liquid tag."""
    return bool(re.search(r'{%\s*tabs\s+', content))


def has_tabs_frontmatter(content: str) -> bool:
    """Check if front matter already has tabs: true."""
    # Match YAML front matter
    frontmatter_match = re.match(r'^---\s*\n(.*?\n)---\s*\n', content, re.DOTALL)
    if not frontmatter_match:
        return False
    
    frontmatter = frontmatter_match.group(1)
    return bool(re.search(r'^tabs:\s*true\s*$', frontmatter, re.MULTILINE))


def add_tabs_frontmatter(content: str) -> str:
    """Add tabs: true to front matter."""
    # Match YAML front matter
    frontmatter_match = re.match(r'^(---\s*\n)(.*?\n)(---\s*\n)', content, re.DOTALL)
    if not frontmatter_match:
        return content
    
    opening = frontmatter_match.group(1)
    frontmatter = frontmatter_match.group(2)
    closing = frontmatter_match.group(3)
    rest = content[frontmatter_match.end():]
    
    # Add tabs: true at the end of front matter
    updated_frontmatter = frontmatter.rstrip('\n') + '\ntabs: true\n'
    
    return opening + updated_frontmatter + closing + rest


def process_file(filepath: Path) -> bool:
    """Process a single file. Returns True if file was modified."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        typer.echo(f"{filepath}: Error reading file: {e}", err=True)
        return False
    
    # Check if file uses tabs but doesn't have tabs: true
    if has_tabs_tag(content) and not has_tabs_frontmatter(content):
        updated_content = add_tabs_frontmatter(content)
        
        try:
            filepath.write_text(updated_content, encoding='utf-8')
            return True
        except Exception as e:
            typer.echo(f"{filepath}: Error writing file: {e}", err=True)
            return False
    
    return False


@app.command()
def main(files: List[Path] = typer.Argument(..., help="Files to process")):
    """Add tabs: true to Jekyll posts that use {% tabs %} liquid tags."""
    modified_files = []
    
    for filepath in files:
        if process_file(filepath):
            modified_files.append(filepath)
    
    if modified_files:
        typer.echo("Added 'tabs: true' to front matter in:", err=True)
        for filepath in modified_files:
            typer.echo(f"  {filepath}", err=True)
        typer.echo("\nPlease review and re-stage these files.", err=True)
        raise typer.Exit(1)
    
    raise typer.Exit(0)


if __name__ == '__main__':
    app()