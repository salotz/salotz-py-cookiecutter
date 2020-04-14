from invoke import task

from ..config import (
    COOKIECUTTER_TEST_DIR,
)

@task
def fill_in(cx):

    # touch them all so they will update
    cx.run("find " + "tests/mock_repos/wumpus/" + " -type f -exec touch {} +")

    # copy update
    cx.run(f"cp -r -u -T tests/mock_repos/wumpus tests/_test_builds/wumpus")

@task(pre=[fill_in])
def init(cx):

    with cx.cd(f"tests/{COOKIECUTTER_TEST_DIR}/wumpus"):
        cx.run("jubeo init --force .")


@task(pre=[init])
def test(cx):

    with cx.cd(f"tests/{COOKIECUTTER_TEST_DIR}/wumpus"):
        cx.run("inv -l")

        # cx.run("inv py.test")
