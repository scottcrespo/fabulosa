from __future__ import with_statement
from fabric.api import run, sudo, local, env, task, cd, settings
from fabric.contrib.console import confirm
from stages import STAGES

@task
def pull(branch=None):
    """
    Fetches from origina and pulls the specified branch.

    Kwargs:
        branch(str): the name of the branch to be pulled

    Usage:
        $ fab <stage> pull

    Example:
        $ fab dev pull:"feature/coolfeature"
    """

    if not branch:
        branch = env.branch

    with cd(env.code_dir):
        run('git fetch && git checkout %s && git pull origin %s' % (branch, branch))

#===================================================================================#

@task
def test():
    """
    Runs tests on the server. If a test fails, then the user will be prompted to
    abort

    Kwargs:

    """

    with settings(warn_only=True):
        with cd(env.code_dir):
            result = run('./manage.py test')
    if result.failed and not confirm("Tests failed. Would you like to continue?"):
        abort("Aborting...")

#===================================================================================#

@task
def reloadit():
    """
    Reloads the apache server

    Usage:
        fab <stage> reloadit
    """

    sudo("service apache2 reload")

#===================================================================================#

@task(default=True)
def deploy(branch=None):
    """
    Pulls the desired branch, runs tests, and reloads the server.

    Usage:
        $ fab <stage> deploy

    """
    if not branch:
        local_branch = STAGES['local']['branch']
    else:
        local_branch = branch
    local("git push origin %s" % local_branch)
    pull(branch)
    test()
    reloadit()

#===================================================================================#

@task(alias='qd')
def quick_deploy(branch=None):
    """
    Deploys without running tests

    Usage:
        $fab <stage> quick_deploy

    Example:
        $ fab dev quick_deploy:"feature/coolbranch"
    """

    if not branch:
        local_branch = STAGES['local']['branch']
    else:
        local_branch = branch
    local("git push origin %s" % local_branch)
    pull(branch)
    reloadit()

#===================================================================================#
