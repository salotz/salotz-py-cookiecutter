from invoke import task

import sys
import os
import os.path as osp
from pathlib import Path


PYTHON_VERSION = '{{ cookiecutter.pyversion }}'

BENCHMARK_STORAGE_URL="./metrics/benchmarks"
BENCHMARK_STORAGE_URI="\"file://{}\"".format(BENCHMARK_STORAGE_URL)


VENV_DIR = "_venv"

SELF_REQUIREMENTS = 'self.requirements.txt'

### Environments

def conda_env(cx, name='dev'):

    env_name = f"{{ cookiecutter.project_slug }}.{name}"

    env_spec_path = Path("envs") / name

    cx.run(f"conda create -y -n {env_name} python={PYTHON_VERSION}",
        pty=True)

    # install the conda dependencies
    if osp.exists(f"{env_spec_path}/env.yaml"):
        cx.run(f"conda env update -n {env_name} --file {env_spec_path}/env.yaml")

    # install the extra pip dependencies
    if osp.exists(f"{env_spec_path}/requirements.txt"):
        cx.run(f"$ANACONDA_DIR/envs/{env_name}/bin/pip install -r {env_spec_path}/requirements.txt")

    # install the package itself
    if osp.exists(f"{env_spec_path}/self.requirements.txt"):
        cx.run(f"$ANACONDA_DIR/envs/{env_name}/bin/pip install -r {env_spec_path}/self.requirements.txt")

    print("--------------------------------------------------------------------------------")
    print(f"run: conda activate {env_name}")

def venv_env(cx, name='dev'):

    venv_dir_path = Path(VENV_DIR)
    venv_path = venv_dir_path / name

    env_spec_path = Path("envs") / name

    # ensure the directory
    cx.run(f"mkdir -p {venv_dir_path}")

    # create the env requested
    cx.run(f"python -m venv {venv_path}")

    # then install the things we need
    with cx.prefix(f"source {venv_path}/bin/activate"):

        if osp.exists(f"{env_spec_path}/{SELF_REQUIREMENTS}"):
            cx.run(f"pip install -r {env_spec_path}/requirements.txt")

        else:
            print("No requirements.txt found")

        # if there is a 'self.requirements.txt' file specifying how to
        # install the package that is being worked on install it
        if osp.exists(f"{env_spec_path}/{SELF_REQUIREMENTS}"):
            cx.run(f"pip install -r {env_spec_path}/{SELF_REQUIREMENTS}")

        else:
            print("No self.requirements.txt found")

    print("----------------------------------------")
    print("to activate run:")
    print(f"source {venv_path}/bin/activate")

@task
def env(cx, name='dev'):

    env_name = f"{{ cookiecutter.project_slug }}.{name}"

    # choose your method:

    # SNIPPET
    # conda_env(cx, name=name)

    venv_env(cx, name=name)

### Repo

@task(pre=[env,])
def repo_test(cx):

    # TODO: tests to run on the consistency and integrity of the repo

    # prefix all of these tests by activating the dev environment
    with cx.prefix(" {{cookiecutter.project_slug}}.dev"):
        cx.run("conda activate {{cookiecutter.project_slug}}.dev && inv -l",
               pty=True)

### Dependencies
# managing dependencies for the project at runtime

## pip: things that can be controlled by pip

# TODO: modify so that it is managing the envs in the 'envs' dir

@task
def deps_pip_pin(cx, name='dev'):

    path = Path("envs") / name

    cx.run("pip-compile "
           f"--output-file={path}/requirements.txt "
           f"{path}/requirements.in")

    # SNIPPET: generate hashes is not working right, or just confusing me
    # cx.run("python -m piptools compile "
    #        "--generate-hashes "
    #        "--output-file=requirements.txt "
    #        f"requirements.in")

@task
def deps_pip_update(cx, name='dev'):

    path = Path("envs") / name

    cx.run("python -m piptools compile "
           "--upgrade "
           f"--output-file={path}/requirements.txt "
           f"{path}/requirements.in")

## conda: managing conda dependencies

# STUB
@task
def deps_conda_pin(cx):
    pass

# STUB
@task
def deps_conda_update(cx):
    pass

# altogether
@task
def deps_pin(cx, name='dev'):

    deps_pip_pin(cx, name=name)

    # SNIPPET
    # deps_conda_pin(cx, name=name)

@task
def deps_pin_update(cx, name='dev'):
    deps_pip_update(cx, name=name)

    # SNIPPET
    # deps_conda_update(cx, name=name)



### Cleaning

@task
def clean_dist(cx):
    """Remove all build products."""

    cx.run("python setup.py clean")
    cx.run("rm -rf dist build */*.egg-info *.egg-info")

@task
def clean_cache(cx):
    """Remove all of the __pycache__ files in the packages."""
    cx.run('find . -name "__pycache__" -exec rm -r {} +')

@task
def clean_docs(cx):
    """Remove all documentation build products"""

    cx.run("rm -rf sphinx/_build/*")

@task
def clean_website(cx):
    """Remove all local website build products"""
    cx.run("rm -rf docs/*")

    # if the website accidentally got onto the main branch we remove
    # that crap too
    for thing in [
            '_images',
            '_modules',
            '_sources',
            '_static',
            'api',
            'genindex.html',
            'index.html',
            'invoke.html',
            'objects.inv',
            'py-modindex.html',
            'search.html',
            'searchindex.js',
            'source',
            'tutorials',
    ]:

        cx.run(f"rm -rf {thing}")

@task(pre=[clean_cache, clean_dist, clean_docs, clean_website])
def clean(cx):
    pass


### Docs

@task
def docs_build(cx):
    """Buld the documenation"""
    cx.run("(cd sphinx; ./build.sh)")

@task(pre=[docs_build])
def docs_serve(cx):
    """Local server for documenation"""
    cx.run("python -m http.server -d sphinx/_build/html")

### TODO: WIP Website

@task(pre=[clean_docs, clean_website, docs_build])
def website_deploy_local(cx):
    """Deploy the docs locally for development. Must have bundler and jekyll installed"""


    cx.cd("jekyll")

    # update dependencies
    cx.run("bundle install")
    cx.run("bundle update")

    # run the server
    cx.run("bundle exec jekyll serve")

# STUB: @task(pre=[clean_docs, docs_build])
@task
def website_deploy(cx):
    """Deploy the documentation onto the internet."""

    cx.run("(cd sphinx; ./deploy.sh)")



### Tests


@task
def tests_benchmarks(cx):
    cx.run("(cd tests/test_benchmarks && pytest -m 'not interactive')")

@task
def tests_integration(cx, node='dev'):
    cx.run(f"(cd tests/test_integration && pytest -m 'not interactive' -m 'node_{node}')")

@task
def tests_unit(cx, node='dev'):
    cx.run(f"(cd tests/test_unit && pytest -m 'not interactive' -m 'node_{node}')")

@task
def tests_interactive(cx):
    """Run the interactive tests so we can play with things."""

    cx.run("pytest -m 'interactive'")

@task()
def tests_all(cx, node='dev'):
    """Run all the automated tests. No benchmarks.

    There are different kinds of nodes that we can run on that
    different kinds of tests are available for.

    - minor : does not have a GPU, can still test most other code paths

    - dev : has at least 1 GPU, enough for small tests of all code paths

    - production : has multiple GPUs, good for running benchmarks
                   and full stress tests

    """


    tests_unit(cx, node=node)
    tests_integration(cx, node=node)

@task
def tests_tox(cx):

    NotImplemented

    TOX_PYTHON_DIR=None

    cx.run("env PATH=\"{}/bin:$PATH\" tox".format(
        TOX_PYTHON_DIR))

### Code Quality

@task
def lint(cx):

    cx.run("rm -f metrics/lint/flake8.txt")
    cx.run("flake8 --output-file=metrics/lint/flake8.txt src/{{ cookiecutter.project_slug }}")

@task
def complexity(cx):
    """Analyze the complexity of the project."""

    cx.run("lizard -o metrics/code_quality/lizard.csv src/{{ cookiecutter.project_slug }}")
    cx.run("lizard -o metrics/code_quality/lizard.html src/{{ cookiecutter.project_slug }}")

    # SNIPPET: annoyingly opens the browser

    # make a cute word cloud of the things used
    # cx.run("(cd metrics/code_quality; lizard -EWordCount src/{{ cookiecutter.project_slug }} > /dev/null)")

@task(pre=[complexity, lint])
def quality(cx):
    pass


### Profiling and Performance

@task
def profile(cx):
    NotImplemented

@task
def benchmark_adhoc(cx):
    """An ad hoc benchmark that will not be saved."""

    cx.run("pytest tests/test_benchmarks")

@task
def benchmark_save(cx):
    """Run a proper benchmark that will be saved into the metrics for regression testing etc."""

    run_command = \
f"""pytest --benchmark-autosave --benchmark-save-data \
          --benchmark-storage={BENCHMARK_STORAGE_URI} \
          tests/test_benchmarks
"""

    cx.run(run_command)

@task
def benchmark_compare(cx):

    # TODO logic for comparing across the last two

    run_command = \
"""pytest-benchmark \
                    --storage {storage} \
                    compare 'Linux-CPython-3.6-64bit/*' \
                    --csv=\"{csv}\" \
                    > {output}
""".format(storage=BENCHMARK_STORAGE_URI,
           csv="{}/Linux-CPython-3.6-64bit/comparison.csv".format(BENCHMARK_STORAGE_URL),
           output="{}/Linux-CPython-3.6-64bit/report.pytest.txt".format(BENCHMARK_STORAGE_URL),
)

    cx.run(run_command)


### Releases


## Pipeline

# Run code quality metrics

# Run Tests

# Run Performance Regressions

## version management

@task
def version_which(cx):
    """Tell me what version the project is at."""

    # get the current version
    import {{ cookiecutter.project_slug }}
    print({{ cookiecutter.project_slug }}.__version__)


@task
def version_set(cx):
    """Set the version with a custom string."""

    print(NotImplemented)
    NotImplemented


# TODO: bumpversion is a flop don't use it. Just do a normal
# replacement or do it manually
@task
def version_bump(cx, level='patch', new_version=None):
    """Incrementally increase the version number by specifying the bumpversion level."""

    print(NotImplemented)
    NotImplemented

    if new_version is None:
        # use the bumpversion utility
        cx.run(f"bumpversion --verbose "
                f"--new-version {new_version}"
                f"-m 'bumps version to {new_version}'"
                f"{level}")

    elif level is not None:
        # use the bumpversion utility
        cx.run(f"bumpversion --verbose "
                f"-m 'bumps version level: {level}'"
                f"{level}")

    else:
        print("must either provide the level to bump or the version specifier")


    # tag the git repo
    cx.run("git tag -a ")



### Packaging

## Building

# IDEA here are some ideas I want to do

# Source Distribution

# Wheel: Binary Distribution

# Beeware cross-patform

# Debian Package (with `dh_virtualenv`)

@task
def update_tools(cx):
    cx.run("pip install --upgrade pip setuptools wheel twine")

@task(pre=[update_tools])
def build_sdist(cx):
    """Make a source distribution"""
    cx.run("python setup.py sdist")

@task(pre=[update_tools])
def build_bdist(cx):
    """Make a binary wheel distribution."""

    cx.run("python setup.py bdist_wheel")

# STUB
@task
def conda_build(cx):

    cx.run("conda-build conda-recipe")

@task(pre=[build_sdist, build_bdist,])
def build(cx):
    """Build all the python distributions supported."""
    pass

## uploading distribution archives

# testing

TESTING_INDEX_URL = "https://test.pypi.org/legacy/"

@task(pre=[update_tools, build])
def test_upload(cx):

    cx.run("twine upload "
           f"--repository-url {TESTING_INDEX_URL} "
           "dist/*")


## Publishing

# PyPI

@task(pre=[build_sdist])
def upload_pypi(cx):
    cx.run('twine upload dist/*')


# Conda Forge

# TODO: convert to the regular conda forge repo when this is finished
@task
def conda_forge_recipe(cx):

    print(NotImplemented)
    NotImplemented

    # TODO: somehow get this path right
    CONDA_FORGE_RECIPE_PATH="../conda-forge_staged_recipe/recipes"
    CONDA_FORGE_HASH_URL=""


    # copy the recipe to the omnia fork
    cx.run(f"cp conda/conda-forge {CONDA_FORGE_RECIPE_PATH}/{{ cookiecutter.project_name }}")

    # commit and push
    cx.run(f"git -C {CONDA_FORGE_RECIPE_PATH} commit -m 'update recipe'")
    cx.run(f"git -C {CONDA_FORGE_RECIPE_PATH} push")
    print(f"make a PR for this in the conda-forge conda recipes: {CONDA_FORGE_RECIPE_PATH}")

