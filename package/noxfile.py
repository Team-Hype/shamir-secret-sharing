import nox


@nox.session
def lint(session):
    session.install("cython-lint")
    session.run("cython-lint", "src")

@nox.session(
    python=["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
)
def test(session):
    session.install("pytest")
    session.run("pytest")
