from invoke import task

from datetime import datetime

from cookiecutter.main import cookiecutter


PY_VERSION = "3.7"
PY_ENV_NAME = "salotz-py-cookiecutter.dev"
CLEAN_EXPRESSIONS = [
    "\"*~\"",
]


# NOTE: in the future we will want to support a more general way of
# doing this
def conda_env(cx):

    cx.run(f"conda create -y -n {PY_ENV_NAME} python={PY_VERSION}",
        pty=True)

    cx.run(f"$ANACONDA_DIR/envs/{PY_ENV_NAME}/bin/pip install -r requirements.dev.txt")

    print("--------------------------------------------------------------------------------")
    print(f"run: conda activate {PY_ENV_NAME}")


@task
def env_dev(cx):
    """Recreate from scratch the wepy development environment."""

    conda_env(cx)


@task
def ls_clean(cx):

    for clean_expr in CLEAN_EXPRESSIONS:
        cx.run('find . -type f -name {} -print'.format(clean_expr))

@task
def clean_tests(cx):

    cx.run("rm -rf tests/_test_builds")

@task(pre=[ls_clean, clean_tests])
def clean(cx):

    print("Deleting Targets")
    for clean_expr in CLEAN_EXPRESSIONS:
        cx.run('find . -type f -name {} -delete'.format(clean_expr))

## Testing

# SNIPPET
#@task(pre=[clean], post=[test_rendered_repo])

@task(pre=[clean])
def test_render(cx, default=True, context_file=None):

    cx.run("mkdir -p tests/_test_builds")

    if default:
        cx.run("cookiecutter -f --no-input -o tests/_test_builds/ .")

    # read from a JSON file
    elif context_file is not None:
        assert osp.exists(context_file), f"context file {context_file} doesn't exist"

        cx.run(f"cookiecutter -f --no-input -o tests/_test_builds/ . {context}")

    # otherwise do interactively
    else:
        cx.run("cookiecutter -f -o tests/_test_builds/ .")


@task(pre=[test_render])
def test_rendered_repo(cx, default=True, context=None):

    default_name = "default_repo_name"
    target_dir = f'tests/_test_builds/{default_name}'

    with cx.cd(target_dir):

        print("testing the generated repo is okay")
        print(f"cd {target_dir}")
        cx.run("inv repo-test", echo=True)
