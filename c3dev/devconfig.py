import configparser
import pathlib
import sys

import click

from .util import exec_command


def config_jupyter_plotly():
    if not sys.platform == "win32":
        environ = "NODE_OPTIONS=--max-old-space-size=4096"
    else:
        environ = ""
    installs = [
        "@jupyter-widgets/jupyterlab-manager",
        "plotlywidget",
        "jupyterlab-plotly",
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
@click.argument("c3dev_dir", type=click.Path(exists=True))
@click.argument("cogent3_dir", type=click.Path(exists=True))
@click.option("-sj", "--skip_jupyter", is_flag=True, help="skip jupyter config")
def main(c3dev_dir, cogent3_dir, skip_jupyter):
    """installs jupyter plotly extensions, then configures mercurial.
       Warning: overwrites .git pre-commit and pre-push hooks"""
    c3dev_path = pathlib.Path(c3dev_dir).resolve()
    cogent3_path = pathlib.Path(cogent3_dir).resolve()
    if not skip_jupyter:
        config_jupyter_plotly()

    if (c3dev_path / ".hg").exists():
        # precommit hooks for c3dev hgrc
        hg_pyco3 = {"hooks": {}}
        hg_pyco3["hooks"]["precommit.black"] = "black " + c3dev_path.name
        hg_pyco3["hooks"]["precommit.isort"] = "isort -rc " + c3dev_path.name
        pyco_path = c3dev_dir / ".hg/hgrc"
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
                "isort -rc " + c3dev_path.name,
            ]
        )
        f.close()
        if not sys.platform == "win32":
            exec_command("chmod +x " + str(pyco3_pre_commit.absolute()))

    if (cogent3_path / ".hg").exists():
        # precommit hooks for cogent3 hgrc
        cogent3 = {"hooks": {}}
        cogent3["hooks"]["pre-push"] = "tox -e py37"
        cogent3["hooks"]["precommit.black"] = "black tests src/" + cogent3_path.name
        cogent3["hooks"]["precommit.isort"] = "isort -rc tests src/" + cogent3_path.name
        cogent3path = cogent3_path / ".hg/hgrc"
        write_config(str(cogent3path), cogent3)

    if pathlib.Path(cogent3_path / ".git").exists():
        # prepush hooks for c3dev git config
        cogent3_pre_push = cogent3_path / ".git/hooks/pre-push"
        f = open(cogent3_pre_push, "w")
        f.writelines(["#!/bin/bash\n", "tox -e py37"])
        f.close()
        if not sys.platform == "win32":
            exec_command("chmod +x " + str(cogent3_pre_push.absolute()))

        # precommit hooks for c3dev git config
        cogent3_pre_commit = cogent3_path / ".git/hooks/pre-commit"
        f = open(cogent3_pre_commit, "w")
        f.writelines(
            [
                "#!/bin/bash\n",
                "black tests src/" + cogent3_path.name + "\n",
                "isort -rc tests src/" + cogent3_path.name,
            ]
        )
        f.close()
        if not sys.platform == "win32":
            exec_command("chmod +x " + str(cogent3_pre_commit.absolute()))


if __name__ == "__main__":
    main()
