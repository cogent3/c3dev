import pathlib
import click


@click.command()
@click.option('-d', '--test_dir',
              type=click.Path(exists=True),
              help='root directory for tests')
@click.option('-a', '--alltests',
              type=click.Path(exists=True),
              help='file containing test suite')
def main(test_dir, alltests):
    """identifies nominal test files not included in the test suite"""
    if not test_dir.endswith('/'):
        test_dir += '/'  # just simplifies subsequent logic

    test_modules = []
    for path in pathlib.Path(test_dir).rglob('test*.py'):
        path = '.'.join(path.relative_to(test_dir).parts)
        path = path.replace('.py', '')
        test_modules.append(path)

    test_suite = pathlib.Path(alltests).read_text()
    rows = []
    for module in test_modules:
        if module not in test_suite:
            rows.append(module)

    if rows:
        click.secho('The following are not part of the test suite:\n',
                    fg='red')
        click.secho('\n'.join(rows), fg='red')
    else:
        click.secho('All test files are included!', fg='blue')

def checkTestFileIntegrity(filepath):
    """Checks: (1) method indentation; (2) crippled tests; (3) commented tests"""

    failed_lines = []
    with open(filepath) as f:

        class_indent = -1
        funct_indent = -1
        multi_comment = False

        for line in f:
            sline = line.lstrip(' ')
            cur_indent = len(line) - len(sline)
            if sline.startswith('class'):
                class_indent = cur_indent
                funct_indent = -1
            if sline.startswith('def'):
                if cur_indent == 0:
                    failed_lines.append('Not in class: ' + sline)
                elif funct_indent == -1:
                    if cur_indent <= class_indent or cur_indent != 4:
                        failed_lines.append('Indentation: ' + sline)
                    else:
                        funct_indent = cur_indent
                elif cur_indent != funct_indent:
                    failed_lines.append('Indentation: ' + sline)

                if not ((sline.startswith('def test_') and sline.find('(self):') != -1) or sline.startswith('def setUp(self):')):
                    failed_lines.append('Crippled: ' + sline)

            if sline.startswith('#') and sline.find('def test_') != -1:
                failed_lines.append('Commented: ' + sline)

            if multi_comment:
                def_pos = sline.find('def test_')
                if def_pos != -1 and def_pos < sline.find('"""'):
                    failed_lines.append('Commented: ' + sline)
            while sline.find('"""') != -1:
                sline = sline[sline.find('"""') + 3:len(sline)]
                multi_comment = not multi_comment

                if multi_comment:
                    def_pos = sline.find('def test_')
                    if def_pos != -1 and def_pos < sline.find('"""'):
                        failed_lines.append('Commented: ' + sline)

        for err in failed_lines:
            print(err.rstrip())


if __name__ == '__main__':
    main()
