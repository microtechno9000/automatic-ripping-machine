#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Automatic-Ripping-Machine Development Tools
    ARM UI management tools
"""
import log
import subprocess


def call_command(command: str, statement: str, func_exit: bool = False):
    """
    Run os commands and check they run
        INPUT: STRING Command, STRING Statement, BOOL Function_Exit (optional)
        OUTPUT: none
    """
    try:
        log.info("-------------------------------------")
        log.info(f"Executing: {command}")
        return_value = subprocess.call(command, shell=True)
        if return_value == 0:
            log.success(statement)
        else:
            log.error(f"Command [{command}] failed with exit code {return_value}")
            if func_exit:
                exit(1)

    except FileNotFoundError as error:
        log.info("\n-------------------------------------")
        log.error(f"Something has gone wrong in executing {command}")
        log.info(f"error - {error}")
        log.info("ARM UI currently stopped, fix error then restart ARM UI")
        log.info("-------------------------------------")
        if func_exit:
            exit(1)
