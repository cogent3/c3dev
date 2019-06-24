import click

from .util import exec_command


@click.command()
def main():
    """launches jupyter lab"""
    cmnd = "cd ~; jupyter lab > /dev/null 2>&1 &"
    r = exec_command(cmnd)


if __name__ == "__main__":
    main()
