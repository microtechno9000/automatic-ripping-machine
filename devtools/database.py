#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Automatic-Ripping-Machine Development Tools
    ARM UI management tools
"""
import os
import armui
import log
import datetime

# DB variables
arm_home = "/home/arm"
path_db = arm_home + "/db/"
file_db = "arm.db"
path_alembic = "/opt/arm/arm/migrations"


def database_backup():
    """
    Backup the arm database file, prior to removing
        INPUT: none
        OUTPUT: none
    """
    try:
        # backup the current ARM DB
        log.info("Backing up the current ARM DB")
        currentime = datetime.datetime.now()
        filename = f"arm_{currentime.year}-{currentime.month}-{currentime.day}_{currentime.hour}{currentime.minute}.db"
        os.system(f"mv {path_db}{file_db} {path_db}{filename}")
        log.success(f"current ARM DB saved {path_db}{filename}")
    except Exception as error:
        log.error("Something has gone wrong, unable backup the database")
        log.error(f" - {error}")
