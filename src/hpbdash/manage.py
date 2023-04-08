#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def is_debugging():
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None


if is_debugging():
    # sys.argv = ['k4k/manage.py', 'load_lessons']
    # sys.argv = ['k4k/manage.py', 'makemigrations']
    # sys.argv = ['k4k/manage.py', 'migrate']
    sys.argv = ['k4k/manage.py', 'runserver']


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hpbdash.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
