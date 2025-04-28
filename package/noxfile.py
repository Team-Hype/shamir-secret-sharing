import nox


@nox.session
def lint(session):
    # Cython-lint for Package
    session.install("cython-lint")
    session.run("cython-lint", "src")

    # Ruff for tests
    session.install("ruff")
    session.run("ruff", "check", "--fix", "tests/")


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def test(session):
    session.install(".")
    session.install("pytest")
    session.run("pytest")
