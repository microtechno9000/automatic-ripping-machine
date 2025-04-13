#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Automatic-Ripping-Machine Development Tools
    pytest the ARM UI
"""
import armui


def ui_test(arm_install: str):
    """
    Run any commands required prior to raising a PR
        INPUT: none
        OUTPUT: to cli
    """
    # Start ARM test db
    armui.call_command("docker compose stop arm-db",
                       "Stopped ARM main DB",
                       func_exit=True)

    # Start ARM test db
    armui.call_command("docker compose start arm-db-test",
                       "Started ARM test DB",
                       func_exit=True)

    # enter virtual environment
    armui.call_command(f"{arm_install}/.venv/bin/python -m pytest test_ui --maxfail=1 -v",
                       "Test executed for ARM UI",
                       func_exit=True)

    # Start ARM test db
    armui.call_command("docker compose stop arm-db-test",
                       "Stopped ARM test DB",
                       func_exit=True)

    # Start ARM test db
    armui.call_command("docker compose start arm-db",
                       "Restarted ARM main DB",
                       func_exit=True)
