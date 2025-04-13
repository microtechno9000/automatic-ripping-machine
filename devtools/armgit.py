#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Automatic-Ripping-Machine Development Tools
    Flake quality checks
"""
import os
import armui
import log


def flake8(arm_path):
    """
    Run quality check against the ARM code and output
        INPUT: path to conduct the check against
        OUTPUT: to cli
    """
    log.info(f"Running quality checks against ARM - {arm_path}")

    flake_config = "--max-complexity=15 --max-line-length=120 --show-source --statistics"

    # Run flake8 against ARM - arm
    code_path = f"{arm_path}/arm"
    armui.call_command(f"{arm_path}/.venv/bin/python -m flake8 {code_path} {flake_config}",
                       f"ARM QA check completed against {arm_path}")

    # Run flake8 against ARM - test_ripper
    code_path = f"{arm_path}/test_ripper"
    armui.call_command(f"{arm_path}/.venv/bin/python -m flake8 {code_path} {flake_config}",
                       f"ARM QA check completed against {code_path}")

    # Run flake8 against ARM - test_ui
    code_path = f"{arm_path}/test_ui"
    armui.call_command(f"{arm_path}/.venv/bin/python -m flake8 {code_path} {flake_config}",
                       f"ARM QA check completed against {code_path}")

    # Run flake8 against ARM - devtools
    code_path = f"{arm_path}/devtools"
    armui.call_command(f"{arm_path}/.venv/bin/python -m flake8 {code_path} {flake_config}",
                       f"ARM QA check completed against {code_path}")


def pr_update():
    """
    Run any commands required prior to raising a PR
        INPUT: none
        OUTPUT: to cli
    """
    log.info("Running scripts to bring ARM up to date")

    # GIT submodule update
    armui.call_command("cd .. & git submodule update --remote", "ARM submodule updated")

    # unittest - ripper
    armui.call_command("python3 -m unittest discover -s /opt/arm/test/unittest -p 'test_ripper*.py' -v",
                       "ARM ripper unittest completed")


def git_branch_change(git_branch, arm_install):
    """Change the git repository branch to another
        INPUT: git_branch
        OUTPUT: none
    """
    if git_branch:
        log.info(f"Change the current git branch to - {git_branch}")

        os.system(f"cd {arm_install}")
        try:
            os.system(f"git checkout {git_branch}")
            log.info(f"ARM branch: {git_branch} checked out")
        except Exception as error:
            log.error(f"Something has gone wrong, unable to check out {git_branch}")
            log.error(f" - {error}")
            log.info("ARM UI currently stopped, fix git error then restart ARM UI")

    else:
        log.error("No branch has been provided")


def arm_clear_data():
    """
    Clear data from the ARM home directory
        INPUT: git_branch
        OUTPUT: none
    """
    # todo, read the location from the arm config file
    # log.console(f"remove data from the home folder: {arm_home}")
    log.info("not currently supported")
