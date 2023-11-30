"""Nox sessions."""

import shutil
import sys
from pathlib import Path

from nox_poetry import Session, session

package = "paper1-code"
owner, repository = "engeir", "paper1-code"
python_versions = ["3.11", "3.12"]


@session(name="pre-commit", python="3.11")
def precommit(session: Session) -> None:
    """Lint using pre-commit.

    Parameters
    ----------
    session : Session
        The Session object.
    """
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    session.install(".")
    session.install(
        "darglint",
        "ruff",
        "pydocstringformatter",
        "mypy",
        "pep8-naming",
        "pre-commit",
        "pre-commit-hooks",
        "pytest",
    )
    session.run("pre-commit", *args)


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy.

    Parameters
    ----------
    session : Session
        The Session object.
    """
    args = session.posargs or ["src", "tests"]
    session.install(".")
    session.install("mypy", "pytest")
    session.install("types-attrs")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite.

    Parameters
    ----------
    session : Session
        The Session object.
    """
    session.install(".")
    session.install("coverage[toml]", "pytest", "pygments")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage")


@session(python="3.11")
def coverage(session: Session) -> None:
    """Produce the coverage report.

    Parameters
    ----------
    session : Session
        The Session object.
    """
    session.run("coverage", "combine")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@session(python=python_versions)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest.

    Parameters
    ----------
    session : Session
        The Session object.
    """
    args = session.posargs or ["all"]
    session.install(".")
    session.install("xdoctest[colors]")
    session.run("python", "-m", "xdoctest", package, *args)


@session(name="docs-build", python="3.11")
def docs_build(session: Session) -> None:
    """Build the documentation.

    Parameters
    ----------
    session : Session
        The Session object.
    """
    args = session.posargs or ["docs", "docs/_build"]
    session.install(".")
    session.install("sphinx", "sphinx-autobuild", "sphinx-rtd-theme")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-apidoc", "-o", "docs", "src")
    session.run("sphinx-build", *args)


@session(python="3.11")
def docs(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes.

    Parameters
    ----------
    session : Session
        The Session object.
    """
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.install(".")
    session.install("sphinx", "sphinx-autobuild", "sphinx-rtd-theme")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-apidoc", "-o", "docs", "src")
    session.run("sphinx-autobuild", *args)
