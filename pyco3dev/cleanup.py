#!/usr/bin/env python

import click, subprocess, os, shutil

@click.command()
@click.argument('dirname', default='.', type=click.Path())
@click.option('-s', '--suffixes', default='', help="file suffix, comma delimit multiple suffixes")
@click.option('-t', '--test', is_flag=True, help="test run")
def main(dirname, suffixes, test):
    endings = ["orig", "rej", "pyc"] + [s.strip() for s in suffixes.split(',')]
    for suffix in endings:
        if test:
            cmnd = 'find %s -name "*.%s"' % (dirname, suffix)
        else:
            cmnd = 'find %s -name "*.%s" -delete' % (dirname, suffix)
        
        paths = subprocess.check_output(cmnd, shell=True)
        if test and paths:
            print(paths)

    cmnd = 'find %s -name "__pycache__"' % dirname
    paths = subprocess.check_output(cmnd, shell=True)
    for path in paths.splitlines():
        if test:
            print(path)
        else:
            shutil.rmtree(path)

if __name__ == "__main__":
    main()