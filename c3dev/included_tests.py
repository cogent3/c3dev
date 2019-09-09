import pathlib

import click


@click.command()
@click.option(
    "-d", "--test_dir", type=click.Path(exists=True), help="root directory for tests"
)
@click.option(
    "-a", "--alltests", type=click.Path(exists=True), help="file containing test suite"
)
def main(test_dir, alltests):
    """identifies nominal test files not included in the test suite"""
    if not test_dir.endswith("/"):
        test_dir += "/"  # just simplifies subsequent logic

    test_modules = []
    for path in pathlib.Path(test_dir).rglob("**/test*.py"):
        path = ".".join(path.relative_to(test_dir).parts)
        path = path.replace(".py", "")
        test_modules.append(path)

    test_suite = pathlib.Path(alltests).read_text()
    rows = []
    for module in test_modules:
        if module not in test_suite:
            rows.append(module)

    if rows:
        click.secho("The following are not part of the test suite:\n", fg="red")
        click.secho("\n".join(rows), fg="red")
    else:
        click.secho("All test files are included!", fg="blue")


if __name__ == "__main__":
    main()
