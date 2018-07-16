#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import threading
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

try:
    from config import config as CONFIG
except ImportError:
    print("Could not find config file")
    sys.exit(1)

APPS_DIR = os.path.join(BASE_DIR, 'apps')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
TMP_DIR = os.path.join(BASE_DIR, 'tmp')
HTTP_HOST = CONFIG.HTTP_BIND_HOST or '127.0.0.1'
HTTP_PORT = CONFIG.HTTP_LISTEN_PORT or 8080
DEBUG = CONFIG.DEBUG
LOG_LEVEL = CONFIG.LOG_LEVEL

START_TIMEOUT = 15
WORKERS = 4
DAEMON = False

EXIT_EVENT = threading.Event()
ALL_SERVICES = ['gunicorn', 'celery', 'beat']

try:
    os.makedirs(os.path.join(BASE_DIR, "data", "static"))
    os.makedirs(os.path.join(BASE_DIR, "data", "media"))
except:
    pass


def make_migrations():
    print("Check database structure change ...")
    os.chdir(os.path.join(BASE_DIR, 'apps'))
    subprocess.call('python3 manage.py makemigrations', shell=True)

def run_migrate():
    print("Migrate structure changes to database ...")
    os.chdir(os.path.join(BASE_DIR, 'apps'))
    subprocess.call('python3 manage.py migrate', shell=True)


def collect_static():
    print("Collect static files")
    os.chdir(os.path.join(BASE_DIR, 'apps'))
    subprocess.call('python3 manage.py collectstatic --no-input', shell=True)

def prepare():
    make_migrations()
    run_migrate()
    collect_static()



