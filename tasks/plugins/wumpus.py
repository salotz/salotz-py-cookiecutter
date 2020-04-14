from invoke import task

from ..config import (
    COOKIECUTTER_TEST_DIR,
)

ENV = "dev"

@task
def fill_in(cx):

    # touch them all so they will update
    cx.run("find " + "tests/mock_repos/wumpus/" + " -type f -exec touch {} +")

    # copy update
    cx.run(f"cp -r -u -T tests/mock_repos/wumpus tests/_test_builds/wumpus")

@task(pre=[fill_in])
def init(cx):

    # TODO: make temporary env for running the tooling

    with cx.cd(f"tests/{COOKIECUTTER_TEST_DIR}/wumpus"):
        cx.run("jubeo init --force .")
        cx.run("pip install -r .jubeo/requirements.txt")
        cx.run(f"inv env.deps-pin -n {ENV}")
        cx.run(f"inv env -n {ENV}")


@task(pre=[init])
def test(cx):

    with cx.prefix(f"cd tests/{COOKIECUTTER_TEST_DIR}/wumpus && source _venv/dev/bin/activate"):
        cx.run("inv -l")

        #cx.run("inv py.tests-unit")
        cx.run("inv py.tests-integration")