import configparser
import pathlib
import sys

import click

from .util import exec_command


def write_config(path, settings):
    """execute black and isort on commit, run_tests on push"""
    config = configparser.ConfigParser()
    config.read(path)
    for section in settings:
        config[section] = {}
        for key, val in settings[section].items():
            config[section][key] = val
    with open(path, "w") as config_out:
        config.write(config_out)


@click.command()
@click.argument("c3dev_dir", type=click.Path(exists=True))
@click.argument("cogent3_dir", type=click.Path(exists=True))
@click.option("-sv", "--skip_vc", is_flag=True, help="skip version control config")
def main(c3dev_dir, cogent3_dir, skip_vc):
    """installs jupyter plotly extensions, then configures git/hg.
    Warning: overwrites .git pre-commit and pre-push hooks"""
    c3dev_path = pathlib.Path(c3dev_dir).resolve()
    cogent3_path = pathlib.Path(cogent3_dir).resolve()

    if not skip_vc:
        if (c3dev_path / ".hg").exists():
            # precommit hooks for c3dev hgrc
            hg_pyco3 = {"hooks": {}}
            hg_pyco3["hooks"]["precommit.black"] = "black " + c3dev_path.name
            hg_pyco3["hooks"]["precommit.isort"] = "isort " + c3dev_path.name
            pyco_path = c3dev_path / ".hg/hgrc"
            assert pyco_path.exists()
            write_config(str(pyco_path), hg_pyco3)

        if (c3dev_path / ".git").exists():
            # precommit hooks for c3dev git config
            pyco3_pre_commit = c3dev_path / ".git/hooks/pre-commit"
            f = open(pyco3_pre_commit, "w")
            f.writelines(
                [
                    "#!/bin/bash\n",
                    "black " + c3dev_path.name + "\n",
                    "isort " + c3dev_path.name,
                ]
            )
            f.close()
            if not sys.platform == "win32":
                exec_command("chmod +x " + str(pyco3_pre_commit.absolute()))

        if (cogent3_path / ".hg").exists():
            # precommit hooks for cogent3 hgrc
            cogent3 = {"hooks": {}}
            cogent3["hooks"]["pre-push"] = "tox -e py38"
            cogent3["hooks"]["precommit.black"] = "black tests/ src/"
            cogent3["hooks"]["precommit.isort"] = "isort tests/ src/"
            cogent3["hooks"]["pre-push.bookmark"] = "hg bookmark -fr default develop"
            cogent3path = cogent3_path / ".hg/hgrc"
            write_config(str(cogent3path), cogent3)

        if pathlib.Path(cogent3_path / ".git").exists():
            # prepush hooks for c3dev git config
            cogent3_pre_push = cogent3_path / ".git/hooks/pre-push"
            f = open(cogent3_pre_push, "w")
            f.writelines(["#!/bin/bash\n", "tox -e py38"])
            f.close()
            if sys.platform != "win32":
                exec_command("chmod +x " + str(cogent3_pre_push.absolute()))

            # precommit hooks for c3dev git config
            cogent3_pre_commit = cogent3_path / ".git/hooks/pre-commit"
            f = open(cogent3_pre_commit, "w")
            f.writelines(
                [
                    "#!/bin/bash\n",
                    "black tests/ src/\n",
                    "isort tests/ src/\n",
                ]
            )
            f.close()
            if sys.platform != "win32":
                exec_command("chmod +x " + str(cogent3_pre_commit.absolute()))


if __name__ == "__main__":
    main()
