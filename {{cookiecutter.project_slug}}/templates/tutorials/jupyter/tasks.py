from invoke import task

import os
import os.path as osp
from pathlib import Path

@task
def init(cx):
    cx.run("mkdir -p _output")
    cx.run("mkdir -p _tangle_source")

@task
def clean(cx):
    cx.run("rm -rf _output/*")
    cx.run("rm -rf _tangle_source/*")

@task(pre=[init])
def tangle(cx):
    cx.run("jupyter-nbconvert --to 'python' --output-dir=_tangle_source README.ipynb")
    cx.run(f"chmod ug+x ./_tangle_source/*.py", warn=True)

@task
def clean_env(cx):
    cx.run("rm -rf _env")

@task(pre=[init])
def env(cx):
    """Create the environment from the specs in 'env'. Must have the
    entire repository available as it uses the tooling from it.

    """

    example_name = Path(os.getcwd()).stem

    with cx.cd("../../../"):
        cx.run(f"inv docs.env-example -n {example_name}")
