from invoke import task

@task
def init(cx):
    cx.run("mkdir -p _output")

@task
def clean(cx):
    cx.run("rm -rf _output")

@task(pre=[init])
def tangle(cx):

    raise NotImplementedError("Not implemented yet.")
