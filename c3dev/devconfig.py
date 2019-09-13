import configparser
import pathlib

import click

from .util import exec_command


def config_jupyter_plotly():
    environ = "NODE_OPTIONS=--max-old-space-size=4096"
    installs = [
        "@jupyter-widgets/jupyterlab-manager",
        "plotlywidget",
        "@jupyterlab/plotly-extension",
        "jupyterlab-chart-editor",
    ]
    for install in installs:
        cmnd = f"{environ} jupyter labextension install {install}  --no-build"
        r = exec_command(cmnd)
    # then do install
    cmnd = "jupyter lab build"
    r = exec_command(cmnd)


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
@click.argument("root_dir", type=click.Path(exists=True))
@click.option("-sj", "--skip_jupyter", is_flag=True, help="skip jupyter config")
def main(root_dir, skip_jupyter):
    """installs jupyter plotly extensions, then configures mercurial"""
    root_dir = pathlib.Path(root_dir)
    if not skip_jupyter:
        config_jupyter_plotly()

    if pathlib.Path(root_dir / "c3dev/.hg").exists():
        # precommit hooks for c3dev hgrc
        hg_pyco3 = {"hooks": {}}
        hg_pyco3["hooks"]["precommit.black"] = "black c3dev/"
        hg_pyco3["hooks"]["precommit.isort"] = "isort -rc c3dev/"
        pyco_path = root_dir / "c3dev/.hg/hgrc"
        assert pyco_path.exists()
        write_config(str(pyco_path), hg_pyco3)

    if pathlib.Path(root_dir / "c3dev/.git").exists():
        # precommit hooks for c3dev git config
        pyco3_pre_commit = root_dir / "c3dev/.git/hooks/pre-commit"
        f = open(pyco3_pre_commit, "w")
        f.writelines([
            "#!/bin/bash",
            "black c3dev/",
            "isort -rc c3dev/",
        ])
        f.close()

    if pathlib.Path(root_dir / "PyCogent3Apps/.hg").exists():
        # precommit hooks for cogent3 hgrc
        cogent3 = {"hooks": {}}
        cogent3["hooks"]["pre-push"] = "tox -e py37"
        cogent3["hooks"]["precommit.black"] = "black src/cogent3/ tests/"
        cogent3["hooks"]["precommit.isort"] = "isort -rc src/cogent3/ tests/"
        cogent3path = root_dir / "PyCogent3Apps/.hg/hgrc"
        write_config(str(cogent3path), cogent3)

    if pathlib.Path(root_dir / "PyCogent3Apps/.git").exists():
        # prepush hooks for c3dev git config
        cogent3_pre_push = root_dir / "PyCogent3Apps/.git/hooks/pre-push"
        f = open(cogent3_pre_push, "w")
        f.writelines([
            "#!/bin/bash",
            "tox -e py37",
        ])
        f.close()
        # precommit hooks for c3dev git config
        cogent3_pre_commit = root_dir / "PyCogent3Apps/.git/hooks/pre-commit"
        f = open(cogent3_pre_commit, "w")
        f.writelines([
            "#!/bin/bash",
            "black src/cogent3 tests/",
            "isort -rc src/cogent3/ tests/",
        ])
        f.close()


if __name__ == "__main__":
    main()
