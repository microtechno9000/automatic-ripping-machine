#!/bin/bash

# ARM_CODE is set in the arm_setup_ui.sh as a global value

ARM_UI=${ARM_CODE}/arm/runui.py

echo "Starting ARM Web Interface - user [${ARM_UID}] - script [${ARM_UI}]"
chmod +x ${ARM_UI}
exec /sbin/setuser arm /bin/python3 ${ARM_UI}