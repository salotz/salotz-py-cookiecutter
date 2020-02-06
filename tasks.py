from invoke import task

from datetime import datetime

from cookiecutter.main import cookiecutter


PY_VERSION = "3.7"
PY_ENV_NAME = "salotz-py-cookiecutter.dev"
CLEAN_EXPRESSIONS = [
    "\"*~\"",
]

@task
def render(cx):

    render_date = datetime.utcnow()

    context = {
        'render_year' : render_date.year,
        'render_timestamp' : render_date.isoformat()
    }

    cookiecutter('.',
                 extra_context=context)

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

@task(ls_clean)
def clean(cx):
    print("Deleting Targets")
    for clean_expr in CLEAN_EXPRESSIONS:
        cx.run('find . -type f -name {} -delete'.format(clean_expr))
