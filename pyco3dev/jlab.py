import click
from subprocess import Popen, PIPE


@click.command()
def main():
    '''launches jupyter lab'''
    cmnd = "cd ~; jupyter lab > /dev/null 2>&1 &"
    proc = Popen(cmnd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        msg = err
        sys.stderr.writelines('FAILED: %s\n%s' % (cmnd, msg))
        sys.exit(proc.returncode)
    if out is not None:
        r = out.decode('utf8')
        click.secho(r, fg='red')
    else:
        r = None
    return r

if __name__ == "__main__":
    main()
