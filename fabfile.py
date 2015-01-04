from fabric.api import local, run, lcd, cd, env
from os.path import exists as file_exists
from fabtools.python import install, is_installed, virtualenv, install_requirements
from os import path
import json


PWD = path.dirname(__file__)
VENV_DIR = path.join(PWD, '.env')
DEV_ENV_DIR = path.join(PWD, '.denv')


def require_dep(name):
    local('pip install %s' % name)


def dev():
    # Allow this to persist, since we aren't as rigorous about keeping state clean
    if not file_exists('.denv'):
        local('virtualenv .denv')
 
    with virtualenv(DEV_ENV_DIR):
        local('pip install -r dev-requirements.txt')


def sdist():
    if file_exists('dist/'):
        local('rm -rf dist/')
    local('mkdir dist')
    with virtualenv(VENV_DIR):
        local('python setup.py sdist')


def publish():
    with virtualenv(VENV_DIR):
        local('python setup.py register')
        local('twine upload dist/*.tar.gz')


def setup():
    if file_exists('.env'):
        local('rm -rf .env')
    local('virtualenv .env')
    with virtualenv(VENV_DIR):
        local('pip install --upgrade setuptools')


def install():
    with virtualenv(VENV_DIR):
        local('pip install dist/*.tar.gz')
        local('pip install pytest')


def make():
    with virtualenv(DEV_ENV_DIR):
        with lcd(path.dirname(__file__)):
            local('python dev_setup.py build_ext --inplace > /dev/null')


def test():
    with virtualenv(VENV_DIR):
        with lcd(path.dirname(__file__)):
            local('py.test -x')


def docs():
    with lcd('docs'):
        local('make html')
