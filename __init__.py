"""
.. module:: __init__.py
    :platform: Unix
    :synopsis: Fabfile manage deployment stages
        `Read The Docs <http://fabric.readthedocs.org`_
    
.. moduleauthor:: Scott Crespo <scottc@tricyclestudios.com>
"""

from __future__ import with_statement

from fabric.api import run, local, env, cd, sudo, settings, task

from stages import localenv, develop, production, stage_set
from deploy import pull, test, deploy, quick_deploy, reloadit

stage_set()

@task
def cmd(command, as_sudo=False, venv=True):
    """
    Runs a command on the environment from the project's root directory.
    
    Kwargs:
        command(str): the command you want to execute
        as_sudo(bool): whether the command should be run as sudo
        venv(bool): whether the command should be run with the virtualenv activated
    
    Usage:
        $ fab  <stage> cmd:"<command>"
    
        $ fab <stage> cmd:"pip install -r requirements.txt"
    """
    with cd(env.code_dir):        
        
        if venv==True: 
            run("source env/bin/activate")
        
        if as_sudo:
            mode = sudo
        else:
            mode = run
            
        mode('%s' % command)
