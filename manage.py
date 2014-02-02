#!/usr/bin/env python
import os
import sys

os.environ['X_DJANGO_PROJECT_PATH'] = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
