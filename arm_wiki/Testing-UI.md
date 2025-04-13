# UI Testing in ARM
<!-- TOC -->
* [UI Testing in ARM](#ui-testing-in-arm)
  * [Overview](#overview)
  * [Running the UI Tests](#running-the-ui-tests)
  * [Example Output](#example-output)
<!-- TOC -->

This section outlines how to run and interpret the ARM UI test suite. 

## Overview

The ARM UI tests validate core UI and backend model functionality to ensure stable interactions across:

- Flask blueprints (e.g., 404/500 handlers),
- SQLAlchemy models (e.g., SystemInfo, Config, Job, etc.),
- Alembic versioning,
- UI settings and user creation.

Tests are written using pytest and are designed to be run from within the ARM virtual environment.

## Running the UI Tests

1. Navigate to the ARM code path `/opt/arm`.
2. Activate the ARM virtual environment:

```bash
$ source .venv/bin/activate
```

3. Run the ARM UI tests from within the VENV:

```bash
$ pytest test_ui --maxfail=1 -v
```
pytest automatically runs through all test files and cases within the `test_ui` folder.
The below commands are optional, but provide additional context when testing the code:

* --maxfail=1 - _top after the first failure (optional for debugging)._
* -v - _Verbose mode (shows test names and progress percentages)._

## Example Output

All tests running and passing

```bash
$ pytest test_ui --maxfail=1 -v
================================================== test session starts ===================================================
platform linux -- Python 3.10.17, pytest-8.1.1, pluggy-1.5.0 -- /opt/arm/.venv/bin/python
cachedir: .pytest_cache
rootdir: /opt/arm
collected 16 items                                                                                                       

test_ui/test_bp_errors.py::test_errors_404 PASSED                                                                  [  6%]
test_ui/test_bp_errors.py::test_errors_500 PASSED                                                                  [ 12%]
test_ui/test_model_alembic_version.py::test_query_alembic_version PASSED                                           [ 18%]
test_ui/test_model_config.py::test_create_config PASSED                                                            [ 25%]
test_ui/test_model_config.py::test_query_config PASSED                                                             [ 31%]
test_ui/test_model_job.py::test_create_job PASSED                                                                  [ 37%]
test_ui/test_model_job.py::test_job_attributes PASSED                                                              [ 43%]
test_ui/test_model_notifications.py::test_create_notifications PASSED                                              [ 50%]
test_ui/test_model_notifications.py::test_query_notifications PASSED                                               [ 56%]
test_ui/test_model_system_drives.py::test_create_system_drives PASSED                                              [ 62%]
test_ui/test_model_system_drives.py::test_query_system_drives PASSED                                               [ 68%]
test_ui/test_model_system_info.py::test_create_system_info PASSED                                                  [ 75%]
test_ui/test_model_system_info.py::test_query_system_info PASSED                                                   [ 81%]
test_ui/test_model_ui_settings.py::test_query_ui_settings PASSED                                                   [ 87%]
test_ui/test_model_user.py::test_create_user PASSED                                                                [ 93%]
test_ui/test_model_user.py::test_query_user PASSED                                                                 [100%]

=================================================== 16 passed in 1.20s ===================================================
```