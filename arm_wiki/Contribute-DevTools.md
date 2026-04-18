## Overview
To support development of ARM, some of the more tedious and repetitious development tasks have been wrapped up into the ARM Development Tools. The developer tools (devtools) are designed to help out anyone contributing to ARM and save time when testing out any changes being made.

To run devtools, navigate to the arm devtools folder and run the python file, armdevtools.py.

Running the script requires:
- File set to executable; and
- Python virtual environment setup, see [Python Docs - Creation of virtual environments](https://docs.python.org/3/library/venv.html)

> [!IMPORTANT]
> Executing any docker scripts requires docker permissions, otherwise the scripts will fail

## Running devtools
There are various commands available to aid in development, testing and preperation ahead of merging code into ARM.


### [-h] Help
The below shows the list of available commands devtools provides.

```bash
$ ./armdevtools.py -h
usage: armdevtools.py [-h] [-dr DR] [--clean] [-dc] [--monitor] [-qa] [-pr] [-test_ui] [-v]

Automatic Ripping Machine Development Tool Scripts. Note: scripts assume running on a bare metal server when running, unless running the specific docker rebuild
scripts.

options:
  -h, --help  show this help message and exit
  -dr DR      Docker - Stop, Remove and Rebuild the ARM Docker image, leaving the container
  --clean     Docker - Remove all ARM docker images and containers before rebuilding.
  -dc         Docker-Compose - Remove all ARM docker images using docker-compose, rebuild and start ARM.
  --monitor   Docker-Compose - Set the '-d' status, calling --monitor will not set '-d' and docker will output all text to the console.
  -qa         QA Checks - run Flake8 against ARM
  -pr         Actions to run prior to committing a PR against ARM on github
  -test_ui    Test ARM UI - run pytest against test_ui folder (auto-starts developer db)
  -v          ARM Dev Tools Version
```


### [-dr DR] Docker Rebuild
Following any code changes to ARM, testing the changes in the docker image can be a tedious process.
This command automates some of the process to make that change easier.
To run, pass the configuration file `start_arm_container.sh` to configure the docker run.

Running this command executes the following docker commands.
1. Stops the ARM container
2. Removes the ARM container
3. Rebuilds the ARM container
4. Starts the ARM container, using the provided arm configuration `start_arm_container.sh`

```bash
./armdevtools.py -dr ~/start_arm_container.sh
INFO: Rebuilding docker image post ARM update
INFO: -------------------------------------
INFO: Executing: docker stop automatic-ripping-machine
Error response from daemon: No such container: automatic-ripping-machine
INFO: ARM container stopped     [Ok]
INFO: -------------------------------------
INFO: Executing: docker container rm automatic-ripping-machine
Error: No such container: automatic-ripping-machine
INFO: ARM Docker container deleted      [Ok]
INFO: -------------------------------------
INFO: Executing: docker build -t automatic-ripping-machine /opt/arm
Sending build context to Docker daemon   34.2MB
Step 1/21 : FROM automaticrippingmachine/arm-dependencies:1.1.1 AS base
 ---> 601d89529745
...
Step 21/21 : WORKDIR /home/arm
 ---> Running in 6ed2590d5d46
Removing intermediate container 6ed2590d5d46
 ---> 58b643c79d04
Successfully built 58b643c79d04
Successfully tagged automatic-ripping-machine:latest
INFO: ARM Docker container rebuilt      [Ok]
INFO: -------------------------------------
INFO: Executing: /home/arm/armdocker.bash
ec1f1c857f498c16f5149efaf305ed78828247577dd2c637c4c2bfd81525a449
INFO: ARM Docker container running      [Ok]
```


### [-dr DR --clean] Docker Clean
Runs the below, prior to then building the image as above.

```bash
docker image rm automatic-ripping-machine
```


### [-dc ] Docker Compose
Build ARM using the `docker-compose.yml` configuration.

Running this command executes the following docker commands.
1. Stops the ARM container
2. Removes the ARM container
3. Rebuilds the ARM container
4. Starts the ARM container


### [-dc --monitor] Docker Compose
Runs docker compose without putting to the background via `-d` and will output runtime operations to console.
Useful when debugging rebuilds.


### [-qa] Run Flake8 Check
When a new commit is made against ARM, the [github workflows](https://github.com/automatic-ripping-machine/automatic-ripping-machine/tree/main/.github/workflows) are automatically run against the commit, to ensure the new codes quality and functionality. Running the QA check devtool command runs the same Flake8 check against the '/opt/arm' folder and files prior to commencing any commits and potentially failing the QA checks.
For more details of how Flake8 works can be found at [https://flake8.pycqa.org/en/latest/](https://flake8.pycqa.org/en/latest/).
Running the qa check executes the below command, and if all is good will return no results, as shown below.

`flake8 /opt/arm/arm --max-complexity=15 --max-line-length=120 --show-source --statistics`

*Example Test - Passing*

```bash
./armdevtools.py -qa
INFO: Going to stop ARMUI - requesting sudo
INFO: ARM UI stopped    [Ok]
INFO: Running quality checks against ARM - /opt/arm
INFO: -------------------------------------
INFO: Executing: flake8 /opt/arm/arm --max-complexity=15 --max-line-length=120 --show-source --statistics
INFO: ARM QA check completed    [Ok]
INFO: Going to restart ARMUI - requesting sudo
INFO: ARM UI started    [Ok]
```

*Example Test - Failing*

```bash
$ ./armdevtools.py -qa
INFO: Running quality checks against ARM - /opt/arm
INFO: -------------------------------------
INFO: Executing: /opt/arm/.venv/bin/python -m flake8 /opt/arm/arm --max-complexity=15 --max-line-length=120 --show-source --statistics
/opt/arm/arm/ui/__init__.py:24:1: E302 expected 2 blank lines, found 1
def create_app(config_name=os.getenv("FLASK_ENV", "production")):
^
1     E302 expected 2 blank lines, found 1
ERROR: Command [/opt/arm/.venv/bin/python -m flake8 /opt/arm/arm --max-complexity=15 --max-line-length=120 --show-source --statistics] failed with exit code 1  [Error]
INFO: -------------------------------------
INFO: Executing: /opt/arm/.venv/bin/python -m flake8 /opt/arm/test_ripper --max-complexity=15 --max-line-length=120 --show-source --statistics
INFO: ARM QA check completed against /opt/arm/test_ripper       [Ok]
INFO: -------------------------------------
INFO: Executing: /opt/arm/.venv/bin/python -m flake8 /opt/arm/test_ui --max-complexity=15 --max-line-length=120 --show-source --statistics
INFO: ARM QA check completed against /opt/arm/test_ui   [Ok]
INFO: -------------------------------------
INFO: Executing: /opt/arm/.venv/bin/python -m flake8 /opt/arm/devtools --max-complexity=15 --max-line-length=120 --show-source --statistics
INFO: ARM QA check completed against /opt/arm/devtools  [Ok]
```

### [-pr] Pre-PR Actions
Executes a list of actions required to bring any ARM code up to scratch prior to raising a new PR.
Currently this runs:
- Update Git submodule (ARM dependencies)

```bash
./armdevtools.py -pr
INFO: Going to stop ARMUI - requesting sudo
INFO: ARM UI stopped    [Ok]
INFO: Running scripts to bring ARM up to date
INFO: -------------------------------------
INFO: Executing: cd .. & git submodule update --remote
remote: Enumerating objects: 7, done.
remote: Counting objects: 100% (7/7), done.
remote: Compressing objects: 100% (7/7), done.
remote: Total 7 (delta 2), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (7/7), 3.01 KiB | 770.00 KiB/s, done.
From https://github.com/automatic-ripping-machine/arm-dependencies
 * [new branch]      dependabot/pip/sqlalchemy-2.0.6 -> origin/dependabot/pip/sqlalchemy-2.0.6
   6caa6fb..8029c3e  main                            -> origin/main
Successfully rebased and updated detached HEAD.
Submodule path '../arm-dependencies': rebased into '8029c3ebbe0406d07cf09e277eb17f6978986ee1'
INFO: ARM submodule updated     [Ok]
INFO: Going to restart ARMUI - requesting sudo
INFO: ARM UI started    [Ok]
```

### [-test_ui] ARM Test User Interface
Runs the ARM User Interface (UI) unit tests against the code.
Requires:
- `arm-db-test` running and `arm-db` stopped [handled by script]
- pytest installed

```bash
$ pip3 install -r requirements_ui.txt
```

*Example Passing Test*

```bash
$ ./devtools/armdevtools.py -test_ui
INFO: -------------------------------------
INFO: Executing: docker compose stop arm-db
[+] Stopping 1/1
 ✔ Container arm-db  Stopped                                                                                                                                    0.0s
INFO: Stopped ARM main DB       [Ok]
INFO: -------------------------------------
INFO: Executing: docker compose start arm-db-test
INFO: Started ARM test DB       [Ok]
INFO: -------------------------------------
INFO: Executing: /opt/arm/.venv/bin/python -m pytest test_ui --maxfail=1 -v
======================================================================== test session starts ========================================================================
platform linux -- Python 3.12.3, pytest-8.1.1, pluggy-1.6.0 -- /opt/arm/.venv/bin/python
cachedir: .pytest_cache
rootdir: /opt/arm
collected 16 items

test_ui/test_bp_errors.py::test_errors_404 PASSED                                                                                                             [  6%]
test_ui/test_bp_errors.py::test_errors_500 PASSED                                                                                                             [ 12%]
test_ui/test_model_alembic_version.py::test_query_alembic_version PASSED                                                                                      [ 18%]
test_ui/test_model_config.py::test_create_config PASSED                                                                                                       [ 25%]
test_ui/test_model_config.py::test_query_config PASSED                                                                                                        [ 31%]
test_ui/test_model_job.py::test_create_job PASSED                                                                                                             [ 37%]
test_ui/test_model_job.py::test_job_attributes PASSED                                                                                                         [ 43%]
test_ui/test_model_notifications.py::test_create_notifications PASSED                                                                                         [ 50%]
test_ui/test_model_notifications.py::test_query_notifications PASSED                                                                                          [ 56%]
test_ui/test_model_system_drives.py::test_create_system_drives PASSED                                                                                         [ 62%]
test_ui/test_model_system_drives.py::test_query_system_drives PASSED                                                                                          [ 68%]
test_ui/test_model_system_info.py::test_create_system_info PASSED                                                                                             [ 75%]
test_ui/test_model_system_info.py::test_query_system_info PASSED                                                                                              [ 81%]
test_ui/test_model_ui_settings.py::test_query_ui_settings PASSED                                                                                              [ 87%]
test_ui/test_model_user.py::test_create_user PASSED                                                                                                           [ 93%]
test_ui/test_model_user.py::test_query_user PASSED                                                                                                            [100%]

========================================================================= warnings summary ==========================================================================
test_ui/test_model_system_info.py::test_create_system_info
test_ui/test_model_system_info.py::test_query_system_info
  /opt/arm/test_ui/test_model_system_info.py:62: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    system_info.last_update_time = datetime.datetime.utcnow()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================== 16 passed, 2 warnings in 0.90s ===================================================================
INFO: Test executed for ARM UI  [Ok]
INFO: -------------------------------------
INFO: Executing: docker compose stop arm-db-test
[+] Stopping 1/1
 ✔ Container arm-db-test  Stopped                                                                                                                               0.8s
INFO: Stopped ARM test DB       [Ok]
INFO: -------------------------------------
INFO: Executing: docker compose start arm-db
[+] Running 1/1
 ✔ Container arm-db  Started                                                                                                                                    0.1s
INFO: Restarted ARM main DB     [Ok]

```

### [-v] Devtools version
Reports the current version of devtools

```bash
$ ./armdevtools.py -v
Automatic Ripping Machine (ARM) - armdevtools.py [0.5]
```
