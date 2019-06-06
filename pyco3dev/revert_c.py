import os
import click
from .util import exec_command


@click.command()
@click.option(
    "-p", "--path", type=click.Path(exists=True), default=".", help="path to PyCogent3"
)
def main(path):
    """launches jupyter lab"""
    os.chdir(path)
    cwd = os.getcwd()
    print(cwd)
    cmnd1 = f'find {path} -name "*.c" -print0 | xargs -0 hg revert'
    cmnd2 = f'find {path} -name "*.c.orig" -delete'
    r1 = exec_command(cmnd1)
    r2 = exec_command(cmnd2)


if __name__ == "__main__":
    main()
