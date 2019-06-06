#!/usr/bin/env python
from pathlib import Path
from os.path import join as path_join, basename
import click
import subprocess
import shutil


@click.command()
@click.argument("newdir", required=True, type=click.Path())
@click.argument("dirname", default=".", type=click.Path(exists=True))
@click.option("-c", "--create", is_flag=True, help="creates newdir")
@click.option("-t", "--test", is_flag=True, help="test run")
def main(newdir, dirname, create, test):
    """move mercurial .rej and .orig files in a directory tree to
    another location"""
    rootdir = Path(dirname)
    newdir = Path(newdir)
    if create:
        newdir.mkdir(exist_ok=True)

    all_files = list(rootdir.rglob("*.orig")) + list(rootdir.rglob("*.rej"))
    for path in all_files:
        relative_to = path.relative_to(rootdir)
        outpath = newdir / relative_to
        if test:
            print(f"Moving {path} to {outpath}")
            continue

        outpath.parent.mkdir(parents=True, exist_ok=True)
        path.rename(outpath)


if __name__ == "__main__":
    main()
