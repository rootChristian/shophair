#!/usr/bin/env python
'''
************************************************************************
*************** Author:   Christian KEMGANG NGUESSOP *******************
*************** Project:   shophair                  *******************
*************** Version:  1.0.0                      *******************
************************************************************************
'''

"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Retrieve the 'ENV' environment variable
    env = os.getenv("ENV", "development")  # Defaults to 'development' if not set

    # Configuration for development environment
    if env == "production":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shophair.settings.prod")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shophair.settings.dev")

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
