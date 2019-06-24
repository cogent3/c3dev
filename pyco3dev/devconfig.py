import configparser
import pathlib

import click

from .util import exec_command


def config_jupyter_plotly():
    environ = "NODE_OPTIONS=--max-old-space-size=4096"
    installs = [
        "@jupyter-widgets/jupyterlab-manager@0.38",
        "plotlywidget@0.8.0 --no-build",
        "@jupyterlab/plotly-extension@0.18.2",
        "jupyterlab-chart-editor@1.0",
    ]
    for install in installs:
        cmnd = f"{environ} jupyter labextension install {install}  --no-build"
        r = exec_command(cmnd)
    # then do install
    cmnd = "jupyter lab build"
    r = exec_command(cmnd)


def mercurial_config(path, settings):
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
def main(root_dir):
    """installs jupyter plotly extensions, then configures mercurial"""
    root_dir = pathlib.Path(root_dir)

    config_jupyter_plotly()

    # precommit hooks for pyco3dev hgrc
    hg_pyco3 = {"hooks": {}}
    hg_pyco3["hooks"]["precommit.black"] = "black pyco3dev/"
    hg_pyco3["hooks"]["precommit.isort"] = "isort -rc pyco3dev/"
    pyco_path = root_dir / "pyco3dev/.hg/hgrc"
    assert pyco_path.exists()
    mercurial_config(str(pyco_path), hg_pyco3)

    # precommit hooks for cogent3 hgrc
    cogent3 = {"hooks": {}}
    cogent3["hooks"]["pre-push"] = "./run_tests"
    cogent3["hooks"]["precommit.black"] = "black black cogent3/ tests/"
    cogent3["hooks"]["precommit.isort"] = "isort -rc cogent3/ tests/"
    cogent3path = root_dir / "PyCogent3Apps/.hg/hgrc"
    mercurial_config(str(cogent3path), cogent3)


if __name__ == "__main__":
    main()
