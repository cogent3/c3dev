import pathlib
import click


@click.command()
@click.option('-d', '--test_dir',
              type=click.Path(exists=True),
              help='root directory for tests')
def main(test_dir):
    """identifies nominal test files not included in the test suite"""
    if not test_dir.endswith('/'):
        test_dir += '/'  # just simplifies subsequent logic

    test_modules = []
    for path in pathlib.Path(test_dir).rglob('**/test*.py'):
        print(path.absolute());
        check_test_file_integrity(path.absolute());
        print();


def check_test_file_integrity(filepath):
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
