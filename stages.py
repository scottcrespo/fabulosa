"""
.. module:: stages.py
    :platform: Unix
    :synopsis: Fabric module for selecting which stage to run.

.. moduleauthor:: Scott Crespo <screspo@highcornergroup.com>
"""

from fabric.api import env, task
from fabric.contrib.console import confirm

import sys, os, getpass

STAGES = {

    'local':{
        'hosts':['%s@localhost' % getpass.getuser()],
        'code_dir': '',
        'branch':'develop',
    },
    'develop': {
        'hosts': [''],
        'code_dir': '',
        'branch': 'develop',
    },
}

#===================================================================================#

def stage_set(stage_name='develop'):
    """
    Sets the environment (stage) that fabric should include in the env dictionary.
    The Default stage is develop

    Kwargs:
        stage_name(str): the name of the stage

    """
    env.stage = stage_name
    for option, value in STAGES[env.stage].items():
        setattr(env, option, value)

#===================================================================================#

@task(alias='loc')
def localenv():
    """
    Sets env to the local stage

    USAGE:
        $ fab local <command>
    """
    stage_set('local')

#===================================================================================#

@task(alias='dev')
def develop():
    """
    Sets env to the develop stage

    USAGE:
        $ fab develop <command>
    """
    stage_set('develop')

#===================================================================================#

@task(alias='prod')
def production():
    """
    No production environment currently available
    """
