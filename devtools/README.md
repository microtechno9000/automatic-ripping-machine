# Automatic Ripping Machine (ARM) - Development Tools

## Overview

Development tools to help automate testing and fault-finding when making changes to the ARM main code.
The Aim of this code is to be independent of the main ARM Repo, such that no libraries are pulled into support the test code.
With the intent that it is possible to run the ARM Devtools as a standalone python script.
This is to avoid introducing errors into the main code from the test tool.
Currently, a work in progress.

## Features

- Manage branch changes and the ARMUI
- Docker
    - Rebuild the docker image with updated ARM code
- Database management
    - Remove the database file, test running of ARM on a new system
    - _Note:_ not yet properly implemented
- Quality Checks (runs Flake8 against all arm code)
- PR Checks
    - Run actions prior to commiting a PR
- Test code
  - Test the UI, run python unit tests


## Usage

```bash
$ ./devtools/armdevtools.py -h
usage: armdevtools.py [-h] [-b B] [-dr DR] [--clean] [-dc] [--monitor] [-db_rem] [-qa] [-pr]
                      [-test_ui] [-v]

Automatic Ripping Machine Development Tool Scripts. Note: scripts assume running on a bare metal
server when running, unless running the specific docker rebuild scripts.

options:
  -h, --help  show this help message and exit
  -b B        Name of the branch to move to, example -b v2_devel
  -dr DR      Docker - Stop, Remove and Rebuild the ARM Docker image, leaving the container
  --clean     Docker - Remove all ARM docker images and containers before rebuilding.
  -dc         Docker-Compose - Remove all ARM docker images using docker-compose, rebuild and
              start ARM.
  --monitor   Docker-Compose - Set the '-d' status, calling --monitor will not set '-d' and
              docker will output all text to the console.
  -db_rem     Database tool - remove current arm.db file
  -qa         QA Checks - run Flake8 against ARM
  -pr         Actions to run prior to committing a PR against ARM on github
  -test_ui    Test ARM UI - run pytest against test_ui folder (auto-starts developer db)
  -v          ARM Dev Tools Version
``````

## Requirements

Dev Tools requires the below packages, which when running ARM within a python virtual environment are pulled in already.

* pytest

## Install

No specific installation is required.

## Troubleshooting

Please see the [wiki](https://github.com/automatic-ripping-machine/automatic-ripping-machine/wiki/).

## Contributing

Pull requests are welcome.  Please see the [Contributing Guide](https://github.com/automatic-ripping-machine/automatic-ripping-machine/wiki/Contributing-Guide)

If you set ARM up in a different environment (hardware/OS/virtual/etc.), please consider submitting a howto to the [wiki](https://github.com/automatic-ripping-machine/automatic-ripping-machine/wiki).

## License

[MIT License](../LICENSE)
