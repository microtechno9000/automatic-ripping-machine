#!/bin/bash
# This script is first to run due to this: https://github.com/phusion/baseimage-docker#running_startup_scripts.
#
# It updates the UIG or GID of the included arm user to whatever value the user
# passes at runtime, if the value set is not the default value of 1000
#
# If the container is run again without specifying UID and GID, this script
# resets the UID and GID of all files in ARM directories to the defaults

set -euo pipefail

#DEFAULT_UID=1000
#DEFAULT_GID=1000

# Report User and Group info
echo -e "ARM running as: $(id)"

### Setup Files
# setup needed/expected dirs if not found
SUBDIRS="logs logs/progress db"
for dir in $SUBDIRS ; do
  thisDir="$ARM_HOME/$dir"
  if [[ ! -d "$thisDir" ]] ; then
    echo "Creating dir: $thisDir"
    mkdir -p "$thisDir"
    # Set the default ownership to arm instead of root
    # chown -R $DEFAULT_UID:$DEFAULT_GID "$thisDir"
  fi
done

##### Setup ARM-specific config files if not found
echo "Creating '${ARM_HOME}/config'"
mkdir -p $ARM_HOME/config
CONFS="arm.yaml apprise.yaml"
for conf in $CONFS; do
  thisConf="$ARM_HOME/config/${conf}"
  if [[ ! -f "${thisConf}" ]] ; then
    echo "Config not found! Creating config file: ${thisConf}"
    # Don't overwrite with defaults during reinstall
    cp --no-clobber "${ARM_CODE}/setup/${conf}" "${thisConf}"
  fi
done