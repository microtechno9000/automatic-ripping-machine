#!/bin/bash
# This script is first to run due to this: https://github.com/phusion/baseimage-docker#running_startup_scripts.
#
# It updates the UIG or GID of the included arm user to whatever value the user
# passes at runtime, if the value set is not the default value of 1000
#
# If the container is run again without specifying UID and GID, this script
# resets the UID and GID of all files in ARM directories to the defaults

set -euo pipefail

DEFAULT_UID=1000
DEFAULT_GID=1000
SUBDIRS="logs logs/progress db"
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[34m"
NC="\e[0m"

###
# Function to check if the ARM user has ownership of the requested folder
###
check_folder_ownership() {
    local check_dir="$1"  # Get the folder path from the first argument
    local folder_uid=$(stat -c "%u" "$check_dir")
    local folder_gid=$(stat -c "%g" "$check_dir")

    echo "Checking ownership of $check_dir"

    if [ "$folder_uid" != "$ARM_UID" ] || [ "$folder_gid" != "$ARM_GID" ]; then
        echo -e "---------------------------------------------"
        echo -e "[${RED}ERROR${NC}]: ARM does not have permissions to $check_dir using $ARM_UID:$ARM_GID"
        echo -e "Folder permissions--> $folder_uid:$folder_gid"
        echo -e "Setting new permissions to UID:[${BLUE}$ARM_UID${NC}] and gid: [${BLUE}$ARM_GID${NC}]"
        chown -R $ARM_UID:$ARM_GID $check_dir
        echo -e "[${GREEN}OK${NC}]: Permissions updated"
        echo -e "---------------------------------------------"
    fi

    echo -e "[${GREEN}OK${NC}]: ARM UID and GID set correctly, ARM has access to '$check_dir' using $ARM_UID:$ARM_GID"
}

### Setup User
if [[ $ARM_UID -ne $DEFAULT_UID ]]; then
  echo -e "Updating arm user id from $DEFAULT_UID to $ARM_UID..."
  usermod -u "$ARM_UID" arm
elif [[ $ARM_UID -eq $DEFAULT_UID ]]; then
  echo -e "Updating arm group id $ARM_UID to default (1000)..."
  usermod -u $DEFAULT_UID arm
fi

if [[ $ARM_GID -ne $DEFAULT_GID ]]; then
  echo -e "Updating arm group id from $DEFAULT_GID to $ARM_GID..."
  groupmod -og "$ARM_GID" arm
elif [[ $ARM_GID -eq $DEFAULT_GID ]]; then
  echo -e "Updating arm group id $ARM_GID to default (1000)..."
  groupmod -og $DEFAULT_GID arm
fi

### Setup Files
check_folder_ownership $ARM_HOME
check_folder_ownership $ARM_CODE

# Add ARM code to the safe folders
git config --system --add safe.directory $ARM_CODE

# setup needed directories for the ARM UI
for dir in $SUBDIRS ; do
  thisDir="$ARM_HOME/$dir"
  if [[ ! -d "$thisDir" ]] ; then
    echo "Creating dir: $thisDir"
    mkdir -p "$thisDir"
    # Set the default ownership to arm instead of root
    chown -R $ARM_UID:$ARM_GID "$thisDir"
  fi
done

### Setup ARM-specific config files if not found
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