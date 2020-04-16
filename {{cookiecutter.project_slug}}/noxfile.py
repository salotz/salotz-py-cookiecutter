import nox

@nox.session(
    python=['3.6', '3.7', '3.8', 'pypy3']
)
def test_user(session):
    """Test using basic pip based installation."""

    session.install("-r", ".jubeo/requirements.txt")
    session.install("-r", "envs/test/requirements.in")
    session.install("-r", "envs/test/self.requirements.txt")

    session.run("inv", "py.tests-all")

@nox.session(
    python=['3.6', '3.7', '3.8'],
    venv_backend="conda",
)
def test_user_conda(session):
    """Test with conda as the installer."""

    # install the pip things first
    session.install("-r", ".jubeo/requirements.txt")
    session.install("-r", "envs/test/requirements.in")
    session.install("-r", "envs/test/self.requirements.txt")

    # install conda specific things here

    session.run("inv", "py.tests-all")
