"""Nox sessions."""

import sys

from nox_poetry import Session, session

package = "paper1-code"
owner, repository = "engeir", "paper1-code"
python_versions = ["3.11", "3.12"]


@session(name="pre-commit", python=python_versions)
def precommit(session: Session) -> None:
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    session.install(".")
    session.install(
        "pydoclint",
        "ruff",
        "pydocstringformatter",
        "mypy",
        "pre-commit",
        "pre-commit-hooks",
        "pytest",
    )
    session.run("pre-commit", *args)


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    session.install(".")
    session.install("mypy", "pytest")
    session.install("types-attrs")
    session.run("mypy")
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install("pytest", ".")
    session.run("pytest")


@session(python=python_versions)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install(".")
    session.install("xdoctest[colors]")
    session.run("python", "-m", "xdoctest", package, *args)
