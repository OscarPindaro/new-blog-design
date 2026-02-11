#!/usr/bin/env python3
"""Add tabs: true to Jekyll posts that use {% tabs %} liquid tags."""

import sys
import re
from pathlib import Path
from typing import List

import typer


app = typer.Typer(add_completion=False)


def has_tabs_tag(content: str) -> bool:
    """Looks for in 'content' if there is a tabs liquid tag.
    this tag is in this format:
    {%<any amount of whitespaces>tabs<anyamount of whitespaces>%}

    as you can see the regex works even without specificing the last two '%}' characters.
    To be fair, possible bugs could originate from this. """
    return bool(re.search(r'{%\s*tabs\s+', content))


def has_tabs_frontmatter(content: str) -> bool:
    """checks if the frontmatter of a jekyll document has a fronmatter.

    a frontmatter is 3 dashes, with anything after, and then 3 dashes again. there
    can be whitespaces.

    If it's not present return False, otherwise, check if 'tabs: true' is present.
    """
    # Match YAML front matter
    frontmatter_match = re.match(r'^---\s*\n(.*?\n)---\s*\n', content, re.DOTALL)
    if not frontmatter_match:
        return False

    frontmatter = frontmatter_match.group(1)
    return bool(re.search(r'^tabs:\s*true\s*$', frontmatter, re.MULTILINE))


def add_tabs_frontmatter(content: str) -> str:
    """if there is not a frontmatter, it returns the original text as is.
    Probably in the future this behaviour will change.

    Frontmatter is the second matched group (.*?\n)
    At the end of it let's add on a new line 'tabs: true\n'

    Finally, concatenated all the group. don't know what that .end() is.
    """
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
    """ Opens a file and adds, if missing, the tabs: true argument if conditions are met.

    By default it checks if the file contains the 'tabs' liquid tag. if it does not have the frontmatter,
    it automatically adds it.

    then, writes the new string at the original path location.
    """
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
