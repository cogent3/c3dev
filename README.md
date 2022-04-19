# Installation

I assume you have cloned this repo (and the one for cogent3) to your local machine.

More details are on the [c3dev wiki](https://github.com/cogent3/c3dev/wiki/Installing-Cogent3-for-development).

## If you use conda

```bash
$ cd path/to/repos/c3dev
$ conda env create -f c3dev_environment.yml
```
will install the command line scripts into the active conda environment.

Then

```bash
$ cd path/to/repos/cogent3
$ flit install --deps all -s --python `which python`
```

installs `cogent3` and all optional dependencies.

## Non-conda

```bash
$ cd path/to/repos/c3dev
$ pip install -e .
```
followed by

```bash
$ cd path/to/repos/cogent3
$ flit install --deps all -s --python `which python`
```
