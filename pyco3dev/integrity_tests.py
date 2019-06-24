import pathlib
from difflib import SequenceMatcher

import click


@click.command()
@click.option(
    "-d", "--test_dir", type=click.Path(exists=True), help="root directory for tests"
)
def main(test_dir):
    """verifies test files included in the test suite"""
    if not test_dir.endswith("/"):
        test_dir += "/"  # just simplifies subsequent logic

    for path in pathlib.Path(test_dir).rglob("**/test*.py"):
        check_test_file_integrity(path.absolute())
        print()


def check_test_file_integrity(filepath):
    """Checks: (1) method indentation; (2) crippled tests; (3) commented tests"""

    failed_lines = []
    with open(filepath) as f:

        for l in f:
            line = l.lstrip(" ")
            cur_indent = len(l) - len(line)
            if line.startswith("def"):
                if cur_indent == 0 and line.find("test_") != -1:
                    failed_lines.append("Not in class: " + line)
                if cur_indent != 4 and line.find("test_") != -1:
                    failed_lines.append("Indentation: " + line)

                if line.startswith("def ") and line.find("_") != -1:
                    possible_test = line[4 : line.find("_")]
                    delta = SequenceMatcher(None, possible_test, "test").ratio()
                    if 0.7 < delta < 1.0:  # can tweak this
                        failed_lines.append("Crippled: " + line)

            if line.startswith("#") and line.find("def test_") != -1:
                failed_lines.append("Commented: " + line)

        print(
            str(filepath.absolute()) + ": ok!"
            if len(failed_lines) == 0
            else ": warnings"
        )

        for err in failed_lines:
            print(err.rstrip())
        if len(failed_lines) == 0:
            print("ok!")


if __name__ == "__main__":
    main()
